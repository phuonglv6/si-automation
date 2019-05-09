import os
from flask import Blueprint, redirect, url_for, render_template,request,jsonify,Response,flash,current_app
from werkzeug.utils import secure_filename

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)


@main_blueprint.route('/')
def index():
    return render_template('extractor/index.html')

@main_blueprint.route('/upload/',methods=('GET', 'POST'))
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        message = dict()
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            uploaded_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            message['filename'] = filename
            message['file_path'] = uploaded_path
            resp = jsonify(message)
            resp.status_code = 200    
        else:
            message.update({'error': 'SI File type is not supported yet'})
            resp = jsonify(message)
            resp.status_code = 500 
        return resp
    else:
        Response(status=418)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']