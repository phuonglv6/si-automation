import datetime
import os
import json
import cv2
from sqlalchemy import func
from flask import render_template, Blueprint, flash, redirect, url_for, session, current_app, abort, request, get_flashed_messages,jsonify
from flask_login import login_required, current_user
from ...core.si_extractor import extract_text,extract_file
from ...util.consts import WIDTH_FOR_ANNOTATION,HEIGHT_FOR_ANNOTATION,WIDTH_FOR_EXTRACTION,HEIGHT_FOR_EXTRACTION,SIBL_CLASSES,MEDIA_DIR
from pathlib import Path

annotation_blueprint = Blueprint(
    'annotation',
    __name__,
    template_folder='../templates/annotation',
    url_prefix="/annotation/"
)
WIDTH     = WIDTH_FOR_ANNOTATION
HEIGHT    = HEIGHT_FOR_ANNOTATION
A4_WIDTH  = WIDTH_FOR_EXTRACTION
A4_HEIGHT = HEIGHT_FOR_EXTRACTION
classes = SIBL_CLASSES

@annotation_blueprint.route('/process/<int:pk>/',methods=('GET', 'POST'))
def process(pk):
    print("@annotation_blueprint.route")
    if request.method == 'GET':
        data = {'pk': pk, 'classes': classes}
        roots = current_app.config['OUT_EXTRACTION_FOLDER']
        rootPath = os.path.join(roots, str(pk), 'root.txt')
        img_path = os.path.join(MEDIA_DIR, 'annotate', str(pk) + '.png')
        if not Path(os.path.join(MEDIA_DIR, 'annotate')).is_dir():
            os.mkdir(os.path.join(MEDIA_DIR, 'annotate'))

        pages = int(cv2.imread(img_path).shape[0]) / HEIGHT

        if Path(rootPath).is_file():
            data['fields'] = extract_root(rootPath, pages)
        print("@annotation_blueprint.route: data: ",data)

        return render_template('annotation/annotation.html', data=data)
    if request.method == 'POST':
        # TODO: if any uploaded file not extract yet?
        filename = session.get('filename_' + str(pk), None)
        num_pages = session.get('pages_' + str(pk), None)
        if filename is None or num_pages is None:
            print('Annotate complete but missing Uploaded_file')
            img_path = os.path.join(MEDIA_DIR, 'annotate', str(pk) + '.png')
            num_pages = int(cv2.imread(img_path).shape[0]) / HEIGHT
            status = 200
            data = {}
        else:
            del session['pages_' + str(pk)]
            del session['filename_' + str(pk)]

        f_root = os.path.join(current_app.config['OUT_EXTRACTION_FOLDER'],
                              str(pk), 'root.txt')
        f = open(f_root, "w+")
        print("list(request.form.keys(): ",list(request.form.keys()))
        for k_name, cors in json.loads(list(request.form.keys())[0]).items():
            idx = list(classes.keys())[list(classes.values()).index(k_name)]
            for name, cor in cors.items():
                if name == 'x1':
                    x1 = float(cor)
                elif name == 'x2':
                    x2 = float(cor)
                elif name == 'y1':
                    y1 = float(cor)
                elif name == 'y2':
                    y2 = float(cor)
            a = (x1 + x2)/2 / WIDTH
            b = (y1 + y2)/2 / (HEIGHT * num_pages)
            c = (x2 - x1) / WIDTH
            d = (y2 - y1) / (HEIGHT * num_pages)
            f.write(idx + ' ' + str(a) + ' ' + str(b)
                    + ' ' + str(c) + ' ' + str(d) + '\n')

        f.close()
        if filename:
            status, data, _ = extract_file(filename)
        resp = jsonify(data)
        resp.status_code = status 
        return resp

def extract_root(root_path, pages):
    """Take root.txt path with number of pages, return fields cordinate
    """
    with open(root_path, 'r') as file_root:
        fields = []
        for x in file_root:
            field = {}
            tmp = x.split(' ')
            field['name'] = classes[tmp[0]]
            b = list(map(float, tmp[1:]))
            field['x1'] = int((b[0] - b[2] / 2) * WIDTH)
            field['y1'] = int((b[1] - b[3] / 2) * (HEIGHT * pages))
            field['x2'] = int((b[0] + b[2] / 2) * WIDTH)
            field['y2'] = int((b[1] + b[3] / 2) * (HEIGHT * pages))
            fields.append(field)
    return fields
