import os
from flask import Flask,request, render_template
from flask_pymongo import PyMongo
from flask import send_from_directory
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
import numpy as np


def l1_distance(a,b):
    return np.sum(np.abs(a-b))


def extract_features(image, model):
    image = load_img(image, target_size=(120, 120))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
    output = np.array(model.predict(image)).flatten()
    return output


def get_images(image,nsi=20):
    features = extract_features(image,model)
    clusters = db.clusters.find_one()
    clusters.pop("_id")
    distances = [l1_distance(cluster,features) for cluster in clusters.values()]
    cluster = distances.index(min(distances))
    images = db.images.find({"cluster": cluster})
    files = [image["file_name"] for image in images]
    return files


model = ResNet50(weights="imagenet", input_tensor=Input(shape=(120, 120, 3)))
model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/cbir_database"
app.config['UPLOAD_FOLDER'] = "static/uploads"

db = PyMongo(app).db



@app.route('/', methods=['GET', 'POST'])
def testing():
    if request.method == 'POST':
        file = request.files['query_img'] #i don't care about image name uploaded
        nb_pic = request.form['nbrpic']
        save_path=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(save_path)
        files=get_images(save_path,int(nb_pic))
        return render_template("Webapp.html", uploaded_image=file.filename,answers=files)
    else:
        return render_template('Webapp.html')


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__=="__main__":
    app.run(debug=True)

