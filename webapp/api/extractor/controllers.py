import os
import re
from flask import Blueprint, redirect, url_for, render_template,request,jsonify,Response,flash,current_app,session
from werkzeug.utils import secure_filename
from ...core.si_extractor import extract_text,extract_file
from ...util.consts import SIBL_CLASSES
from ..models import Doc
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
        filename = request.form['filename']
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

@extractor_blueprint.route('/main_panel/')
def main_panel():
    return render_template('extractor/main_panel.html')

@extractor_blueprint.route('/list/')
def list():
    # doc = model_to_dict(Doc.objects.all().latest('id'))
    doc= Doc.query.order_by(Doc.id.desc()).first()
    data = {'doc': doc.to_dict(show_all=True)}
    print("Data:",data)
    resp = jsonify(data)
    return resp

@extractor_blueprint.route('/pdf/<int:pk>/')
def pdf(pk):
    print("pdf route")
    # data = Doc.query.filter_by(id=Doc.id).first()
    data = Doc.query.get(pk)
    return render_template('extractor/left_panel.html', data=data)

@extractor_blueprint.route('/preview/<int:pk>/')
def preview(pk):
    # doc = Doc.objects.get(id=pk)
    print("Previvew route")
    doc = Doc.query.get(pk)
    hs_codes = {}
    if doc.hs_code:
        for hs_code in doc.hs_code.split(','):
            hs_code = re.sub(r'\W+', '', hs_code)
            hs_codes[hs_code] = 1

    if doc.bl_type and len(hs_codes) > 0:
        for hs_code in hs_codes.keys():
            if hs_code in doc.bl_type:
                hs_codes[hs_code] = 0

    description_of_goods = doc.description_of_goods
    payment = doc.payment.replace('"', '')
    total_weight = doc.total_weight
    total_measurement = doc.total_measurement
    return render_template('extractor/right_panel.html', data={
                'doc': doc, 'hs_codes': hs_codes,
                'description_of_goods': description_of_goods,
                'payment': payment,
                'total_weight': total_weight,
                'total_measurement': total_measurement
            })

@extractor_blueprint.route('/detail/<int:pk>/',methods=('GET', 'POST'))
def detail(pk):
    if request.method == 'GET':
        doc = Doc.query.get(pk).to_dict(show_all=True)
        data = {'doc': doc}
        resp = jsonify(data)
        return resp

    if request.method == 'POST':
        data = dict()
        name  = request.form['name']
        value = request.form['value']
        doc = Doc.query.filter_by(id=pk).first()
        doc.name =value
        db.session.commit()
        
        data['doc'] = Doc.query.get(pk).to_dict(show_all=True)
        data['POST'] = request.form
        resp = jsonify(data)
        return resp
