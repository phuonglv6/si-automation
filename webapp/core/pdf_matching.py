from pdf2image import convert_from_bytes
from .lib import getTableFromImage, getDistance, hasTable, process_image
import os
import pickle
import numpy as np
import cv2
import pytesseract as pt
from .cropUtils import process_crop_image
from operator import itemgetter  # add to pdfreader
from itertools import groupby
import fitz  # PyMuPDF
from pathlib import Path
from ..library.diffimg import diff
from PIL import Image
from django.conf import settings
from shutil import copyfile

# define some threshold for matching tasks
meanLow = 2
meanDiffThre = 0.3
distLow = 0.004
distHigh = 0.007

MEDIA_DIR = settings.MEDIA_ROOT

# set height, width for resizing img
WIDTH = settings.NGHIA_WIDTH
HEIGHT = settings.NGHIA_HEIGHT
A4_WIDTH = settings.A4_WIDTH
A4_HEIGHT = settings.A4_HEIGHT

# class dict
classes = settings.SIBL_CLASSES


def pdf2img(pdfPath):
    """
    return a gray image array for cv2 processing
    """
    # outName = pdfPath.split('/')[-1].split('.')[0]
    with open(pdfPath, 'rb') as file:
        f = file.read()
        images = convert_from_bytes(f, dpi=200)
        num_pages = len(images)

        full_image = []
        for image in images:
            openCV_img = np.array(image.convert('RGB'))
            # convert RGB to BGR
            openCV_img = openCV_img[:, :, ::-1].copy()
            # convert to grayscale
            openCV_img = cv2.cvtColor(openCV_img, cv2.COLOR_BGR2GRAY)
            openCV_img = cv2.resize(openCV_img, (WIDTH, HEIGHT))

            if full_image == []:
                full_image = openCV_img
            else:
                full_image = np.vstack((full_image, openCV_img))

    return full_image, num_pages


def matchingForm(pdfPath, targetPath):
    """
    input image is table-type only
    return folder name in targetPath if matched else 0
    """
    image, num_pages = pdf2img(pdfPath)
    # img = cv2.resize(img, (WIDTH, HEIGHT))
    raw = image.copy()
    img, joint = getTableFromImage(image)
    if not hasTable(img, joint):
        gray = process_image(image)
        img, _ = getTableFromImage(gray)
    _, folders, _ = next(os.walk(targetPath))
    root = None
    newType = True
    if len(folders):
        chosenFolderPath = ''
        result = 0
        for folder in folders:
            rootPath = os.path.join(targetPath, folder, 'root.pickle')
            if Path(rootPath).is_file():
                with open(rootPath, 'rb') as file:
                    root = pickle.load(file)

                    if img.shape == root.shape:
                        dist = getDistance(root, img)
                        meanRoot = np.mean(root)
                        sub1 = np.subtract(root, img)
                        sub2 = np.subtract(img, root)
                        meanSub = min(np.mean(sub1), np.mean(sub2))
                        if (
                            (meanRoot < meanLow) and
                            (dist < distLow) and
                            (meanSub < meanDiffThre)
                        ) or (
                            (meanRoot >= meanLow) and
                            (dist < distHigh) and
                            (meanSub < meanDiffThre)
                        ):
                            if result == 0:
                                newType = False
                                chosenFolderPath = folder
                                result = 0.7*dist + 0.3*meanSub
                            else:
                                tmp = 0.7*dist + 0.3*meanSub
                                if tmp < result:
                                    result = tmp
                                    chosenFolderPath = folder

    if newType:
        sameTemplateFolder = findSameTemplate(img, targetPath, folders)
        return 0, raw, num_pages, sameTemplateFolder
    else:
        return chosenFolderPath, raw, num_pages, None


def findSameTemplate(img, targetPath, folders):
    """
        Compare 2 pdf to find same the template
        Note: Only kind of the template with Line
    """
    maxAccuracy = 0.01
    sameTemplateFolder = None
    for folder in folders:
        rootPath = os.path.join(targetPath, folder, 'root.pickle')
        if Path(rootPath).is_file():
            with open(rootPath, 'rb') as file:
                rootImg = pickle.load(file)
                value = diff(Image.fromarray(img), Image.fromarray(
                    rootImg), delete_diff_file=True)
                if value < maxAccuracy:
                    maxAccuracy = value
                    sameTemplateFolder = folder
    return sameTemplateFolder


def lineRemove(img):
    mask, _ = getTableFromImage(img, h_size=30, v_size=30)
    return cv2.bitwise_not(cv2.subtract(cv2.bitwise_not(mask), img))


def pdfread(y1, x1, y2, x2, page):
    rect = fitz.Rect(y1, x1, y2, x2)
    words = page.getTextWords()
    words_bbox_resize = [(
        (w[0] + w[2]) / 2 - 1,
        (w[1] + w[3]) / 2 - 1,
        (w[0] + w[2]) / 2 + 1,
        (w[1] + w[3]) / 2 + 1,
        w[4], w[5], w[6], w[7]
    ) for w in words]
    mywords = [w for w in words_bbox_resize if fitz.Rect(w[:4]) in rect]
    mywords.sort(key=itemgetter(3, 0))
    group = groupby(mywords, key=itemgetter(3))
    value = ""

    for _, gwords in group:
        if value == "":
            value = " ".join(w[4] for w in gwords)
        else:
            value = value + '\n' + " ".join(w[4] for w in gwords)

    return value


def extract_value(b, num_pages, HEIGHT, size, doc):
    x = int((float(b[1]) - float(b[3])/2)*HEIGHT*num_pages)
    n_page = int(x/HEIGHT)
    pdf_width = size[n_page][0]
    pdf_height = size[n_page][1]
    y1 = int((float(b[0]) - float(b[2])/2)*pdf_width)
    y2 = int((float(b[0]) + float(b[2])/2)*pdf_width)
    x1 = int((float(b[1]) - float(b[3])/2)*pdf_height*num_pages)
    x1 = x1 - (pdf_height*n_page)
    x2 = int((float(b[1]) + float(b[3])/2)*pdf_height*num_pages)
    x2 = x2 - (pdf_height*n_page)
    page = doc[n_page]
    value = pdfread(y1, x1, y2, x2, page)
    return value


def handleMatchedFile(chosenFolder, targetPath, img, jsonName, pdfPath):
    """
        If match but not have root.txt
            return type number
        else
            return Dict result of OCR
    """
    _, folders, _ = next(os.walk(targetPath))
    doc = fitz.open(pdfPath)
    size = []
    for page in doc:
        pix = page.getPixmap(alpha=False)
        width = pix.width
        height = pix.height
        size.append([width, height])
    num_pages = len(doc)
    dbPath = os.path.join(targetPath, chosenFolder, 'root.txt')

    # test OCR
    if Path(dbPath).is_file():
        f = open(dbPath, "r")
        data = {}
        nonOCR = False
        for x in f:
            key = x.split(' ')[0]
            b = x.split(' ')[1:]
            test_text = extract_value(b, num_pages, HEIGHT, size, doc)
            if test_text != '':
                nonOCR = True
                break
        f.close()
        print('chosenFolder:', chosenFolder)
    else:
        print('Cannot find annotation file in',
              targetPath + '/' + chosenFolder)
        return chosenFolder

    # PDF can SELECT text
    if nonOCR is True:
        print('TEXT**********************************************************')
        f = open(dbPath, "r")
        for x in f:
            tmp = x.split(' ')
            key = tmp[0]
            b = tmp[1:]
            data[classes[key]] = extract_value(
                b, num_pages, HEIGHT, size, doc)
    else:
        print('OCR###########################################################')
        f = open(dbPath, "r")
        for x in f:
            tmp = x.split(' ')
            key = tmp[0]
            b = tmp[1:]
            y1 = int((float(b[0]) - float(b[2])/2)*WIDTH)
            x1 = int((float(b[1]) - float(b[3])/2)*HEIGHT * num_pages)
            y2 = int((float(b[0]) + float(b[2])/2)*WIDTH)
            x2 = int((float(b[1]) + float(b[3])/2)*HEIGHT * num_pages)
            crop = img[x1:x2, y1:y2]

            # added line-removing function
            crop = lineRemove(crop)
            # use tesseract OCR to get text from roi
            txt = pt.image_to_string(crop)
            # added process crop func for sparse text case
            if txt == '':
                crop = process_crop_image(crop)
                txt = pt.image_to_string(crop)

            txt = txt.replace('\n\n', '\n')
            data[classes[key]] = txt

    f.close()

    # handling missing annotation field
    for k in classes.values():
        if k not in data:
            data[k] = ''

    return data


def handleUnmatchedFile(targetPath, img, sameTemplateFolder):
    _, folders, _ = next(os.walk(targetPath))
    # TODO: out folder must not have sub-folder that have name is in alphabet
    newType = str(max(map(int, folders)) + 1)
    newTypePath = os.path.join(targetPath, newType)
    os.mkdir(newTypePath)
    # Check has the same template
    if sameTemplateFolder is not None:
        source_path = os.path.join(targetPath, sameTemplateFolder, 'root.txt')
        if Path(source_path).is_file():
            copyfile(source_path, os.path.join(newTypePath, 'root.txt'))

    # Save IMG to media\annotate
    if not Path(os.path.join(MEDIA_DIR, 'annotate')).is_dir():
        os.mkdir(os.path.join(MEDIA_DIR, 'annotate'))
    img_path = os.path.join(MEDIA_DIR, 'annotate', newType + '.png')
    cv2.imwrite(img_path, img)

    # Save pickle table img
    img1, joint = getTableFromImage(img)
    if not hasTable(img1, joint):
        gray = process_image(img)
        img1, _ = getTableFromImage(gray)
    rootPath = os.path.join(targetPath, newType, 'root.pickle')
    with open(rootPath, 'wb') as handle:
        pickle.dump(img1, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return newType
