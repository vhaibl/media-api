import logging.config
import os
import secrets
import sys
import uuid
from http import HTTPStatus

from flask import Flask, jsonify, request, send_from_directory

import media_logging

logging.config.dictConfig(media_logging.LOGGING)
logger = logging.getLogger('api.upload')

secret = secrets.token_urlsafe(32)

UPLOAD_FOLDER = 'files/'
EXTERNAL_PATH = 'media\\'

app = Flask(__name__)
app.base_dir = sys.path[0]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTERNAL_PATH'] = EXTERNAL_PATH
app.secret_key = secret


@app.route('/', methods=['GET', 'POST'])
def where_missing():
    return jsonify({'error': 'The "where" param is missing'}), HTTPStatus.BAD_REQUEST


@app.route('/<where>/', methods=['POST'])
def upload_file(where):
    if 'photo' in request.files:
        file_type = 'photo'
        folder = 'images'
        return save_file(where, file_type, folder)
    if 'audio' in request.files:
        file_type = 'audio'
        folder = 'images'
        return save_file(where, file_type, folder)

    return jsonify({'result': 'Media file has not sent'}), HTTPStatus.BAD_REQUEST


def save_file(where, file_type, folder):
    if not os.path.exists(os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'], folder, where)):
        os.makedirs(os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'], folder, where))
    try:
        file = request.files[file_type]
        photo_name_file = str(uuid.uuid4()) + f'_{request.files[file_type].filename}'
        file.save(os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'], folder, where, photo_name_file))
        return jsonify(
            {'path': os.path.join(app.config['EXTERNAL_PATH'], folder, where, photo_name_file)}), HTTPStatus.OK
    except Exception as er:
        logger.error(er)
        return jsonify(er), HTTPStatus.BAD_REQUEST


@app.route('/media/<file_type>/<where>/<file>', methods=['GET', 'POST'])
def serve(where, file, file_type):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], file_type, where), file)


if __name__ == '__main__':
    app.run()
