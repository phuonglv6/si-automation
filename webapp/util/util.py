# import os
import cv2
import numpy as np
import math
import scipy.stats
from scipy.ndimage.filters import rank_filter
# import pickle
Theshold = 100
jointThre = 0.0004
maskThreLow = 2.6  # 2.8
maskThreHigh = 0.8


def hasTable(img, joint):
    if np.mean(joint) < jointThre:
        if np.mean(img) >= maskThreLow:
            return True
        return False
    elif np.mean(img) < maskThreHigh:
        return False
    return True


def getTableFromImage(img, h_size=-1, v_size=-1):
    if len(img.shape) == 2:
        gray_img = img
    elif len(img.shape) == 3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh_img = cv2.adaptiveThreshold(
        ~gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

    h_img = thresh_img.copy()
    v_img = thresh_img.copy()
    scale = 15  # play around with this

    # Herizon Line Detect
    if h_size == -1:
        h_size = int(h_img.shape[1]/scale)

    # kernel filter with h_size to detect H_line
    h_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (h_size, 1))
    h_erode_img = cv2.erode(h_img, h_structure, 1)
    h_dilate_img = cv2.dilate(h_erode_img, h_structure, 1)

    # Vertical Line Detect
    if v_size == -1:
        v_size = int(v_img.shape[0] / scale)

    # kernel filter with v_size to detect V_line
    v_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_size))
    v_erode_img = cv2.erode(v_img, v_structure, 1)
    v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)

    mask_img = h_dilate_img + v_dilate_img
    joints_img = cv2.bitwise_and(h_dilate_img, v_dilate_img)

    return mask_img, joints_img


def normalDistribution(x, m, sd):
    return scipy.stats.norm(m, sd).pdf(x)


def getMean(array):
    result = 0.0
    for i in array:
        result += i
    return result/len(array)


def getVariance(array, mean):
    result = 0.0
    n = len(array)
    for i in array:
        result += (i-mean)*(i-mean)
    if n < 30:
        # print(result)
        return math.sqrt(result/(n-1))
    else:
        return math.sqrt(result/n)


def getDistance(A, B):
    newA = np.copy(A)
    newB = np.copy(B)
    if len(newA.shape) != 1:
        newA = A.flatten()
    if len(newB.shape) != 1:
        newB = B.flatten()
    if newA.shape == newB.shape:
        return np.linalg.norm(newA-newB)/len(newA)
    else:
        return None


def reshapeImage(image, width=2500, hight=3300):
    return cv2.resize(image, (width, hight))


def checkMap(distance, m, v):
    p = normalDistribution(distance, m, v)
    if p > Theshold:
        return True
    else:
        return False

width = 700
height = 1000
min_width = 20
min_height = 10
density_threshold = 250
padding_ratio = 0.02
padding_w = int(padding_ratio * width)
padding_h = int(padding_ratio*1.5 * height)
WIDTH = 1600
HEIGHT = 2200



def process_image(image):
    #img_origin = cv2.imread(path)
    img_origin = image


    gray = cv2.resize(img_origin, (width,height),interpolation=cv2.INTER_AREA)
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray[:padding_h] = 255
    gray[-padding_h:] = 255
    gray[:,:padding_w] = 255
    gray[:,-padding_w:] = 255

    edges = cv2.Canny(gray, 100, 200)
    # Remove ~1px borders using a rank filter.
    maxed_rows = rank_filter(edges, -4, size=(1, 20))
    debordered = np.minimum(gray, maxed_rows)


    #############
    N= 5
    #iterations = 3
    kernel = np.zeros((N,N), dtype=np.uint8)
    kernel[(N-1)//2,:] = 1  # Bug solved with // (integer division)

    dilated_image = cv2.dilate(debordered , kernel, iterations=3)

    kernel = np.zeros((N,N), dtype=np.uint8)
    kernel[:,(N-1)//2] = 1  # Bug solved with // (integer division)
    dilated_image = cv2.dilate(dilated_image, kernel, iterations=2)
    dilated_image = dilated_image.astype(np.uint8)
    (contours,_) = cv2.findContours(dilated_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        mrect = cv2.boundingRect(contour)
        if mrect[2] < min_width or mrect[3]< min_height:
            continue

        cv2.rectangle(gray, (mrect[0] ,mrect[1]), (mrect[2]+mrect[0] ,mrect[3]+mrect[1] )
                      , (0,0,255), 1)

    return gray