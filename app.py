import os
import secrets
import sys
import uuid
from http import HTTPStatus

from flask import Flask, jsonify, request, send_from_directory

secret = secrets.token_urlsafe(32)
UPLOAD_FOLDER = 'files/'
EXTERNAL_PATH = 'media\\images\\'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.base_dir = sys.path[0]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTERNAL_PATH'] = EXTERNAL_PATH
app.secret_key = secret


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def where_missing():
    return jsonify({'error': 'The "where" param is missing'}), HTTPStatus.BAD_REQUEST


@app.route('/<where>/', methods=['POST'])
def upload_file(where):
    if not os.path.exists(os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'], where)):
        os.makedirs(os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'], where))
    if 'photo' in request.files:
        try:
            file = request.files['photo']
            photo_name_file = str(uuid.uuid4()) + f'_{request.files["photo"].filename}'
            file.save(os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'], where, photo_name_file))
            return jsonify({'path': os.path.join(app.config['EXTERNAL_PATH'], where, photo_name_file)}), HTTPStatus.OK
        except Exception as er:
            # logger.error(er)
            return jsonify(er), HTTPStatus.BAD_REQUEST
    return jsonify({'result': 'Image file has not sent'}), HTTPStatus.BAD_REQUEST


@app.route('/media/images/<where>/<file>', methods=['GET', 'POST'])
def serve(where, file):
    print(os.path.join(app.config['UPLOAD_FOLDER'], where, file))
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], where), file)


if __name__ == '__main__':
    app.run()
