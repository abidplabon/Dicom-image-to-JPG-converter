import pydicom as dicom
import numpy as np
from PIL import Image
import matplotlib.pylab as plt

# image_path = 'C:\\Users\\User\\Downloads\\CHEST_PA_2577.dcm';
# ds = dicom.dcmread(image_path)
# plt.imshow(ds.pixel_array)

# # specify your image path


#
# ds = dicom.dcmread('C:\\Users\\User\\Downloads\\CHEST_PA_2577.dcm')
#
# new_image = ds.pixel_array.astype(float)
#
# scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
#
# scaled_image = np.uint8(scaled_image)
# final_image = Image.fromarray(scaled_image)
#
# final_image.show()
#
#
#
#

from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

DICOM_EXTENSIONS = set(['dcm'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def dicom_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in DICOM_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    if file and dicom_file(file.filename):
        dicomfilename = secure_filename(file.filename)
        print(dicomfilename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], dicomfilename))
        ds = dicom.dcmread('C:\\Users\\User\\Downloads\\'+dicomfilename)

        new_image = ds.pixel_array.astype(float)

        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0

        scaled_image = np.uint8(scaled_image)
        final_image = Image.fromarray(scaled_image)

        final_image.save('static\\images\\image.jpg')
        finalfilename='image.jpg'

        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=finalfilename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)

if __name__ == "__main__":
    app.run()