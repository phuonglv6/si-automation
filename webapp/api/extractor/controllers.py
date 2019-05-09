import os
from flask import Blueprint, redirect, url_for, render_template,request,jsonify,Response,flash,current_app,session
from werkzeug.utils import secure_filename
from ...core.si_extractor import extract_text,extract_file
from ...util.consts import SIBL_CLASSES

classes = SIBL_CLASSES
extractor_blueprint = Blueprint(
    'extractor',
    __name__,
    template_folder='../templates/extractor',
    url_prefix="/extractor/"
)

@extractor_blueprint.route('/process/',methods=('GET', 'POST'))
def process():
    if request.method == 'POST':
        # from ...core.pdf_matching import classes
        filename=request.form['filename']
        # filename = request.POST['filename']
        status, data, num_pages = extract_file(filename)

        if 'temp_num' in data:
            temp_number = data['temp_num']
            session['filename_' + str(temp_number)] = \
                filename.rsplit('.', 1)[0] + '.pdf'
            session['pages_' + str(temp_number)] = num_pages
        
        resp = jsonify(data)
        resp.status_code = status 
        return resp

