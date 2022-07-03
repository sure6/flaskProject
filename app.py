import os

from PIL import Image
import pytesseract
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # set the destination folder for file uploads
basedir = os.path.abspath(os.path.dirname(__file__))  # gets the absolute path of the current project
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])  # the file suffix allowed to upload


# determine if the file is valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# load webpage
@app.route('/')
def upload_test():
    return render_template('upload.html')


@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # splice into valid folder addresses
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # create folder if it does not exist
    f = request.files['myfile']  # create folder if it does not exist
    if f and allowed_file(f.filename):  # determine if the file type is allowed to be uploaded
        f_name = f.filename
        f.save(os.path.join(file_dir, f_name))  # save the file to the Upload directory
        # the pic access address : http://127.0.0.1:5000/static/upload/1.png
        # build a function that can recoginaze the image and convert img to string, then search answer from internet and so on ...
        text = recognize_imaget_to_string("static/upload/"+f_name)

        dict={"errno": 1, "errmsg": "success", "text": text.strip()}
        return jsonify(dict)
    else:
        return jsonify({"errno": 1001, "errmsg": "failed"})


def recognize_imaget_to_string(image_url):
    im = Image.open(image_url)
    text = pytesseract.image_to_string(im)
    return text

if __name__ == '__main__':
    app.run()
