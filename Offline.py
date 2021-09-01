from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from mlinsights.mlmodel import KMeansL1L2
from pymongo import MongoClient
from tqdm import tqdm
import numpy as np
import sys
import os


def extract_features(image_file, model):
    image = load_img(image_file,target_size=(120,120))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
    output = np.array(model.predict(image))
    output.flatten()
    return output


model = ResNet50(weights="imagenet", input_tensor=Input(shape=(120, 120, 3)))
model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
dirs = "static/photos"
files = os.listdir(dirs)
files_paths=[os.path.join(dirs, file) for file in files]
features=np.array([extract_features(file, model) for file in tqdm(files_paths)]).squeeze()
kml1 = KMeansL1L2(5, norm='L1')
kml1.fit(features)
centers=kml1.cluster_centers_
predictions=kml1.predict(features)

try:
    client = MongoClient('localhost', 27017)
except Exception:
    print("############################################")
    print("Oops! DATABASE IN NOT OPEN")
    print("PLEASE LAUNCH MONGODB AND RETRY   ")
    print("###########################################")
    sys.exit(1)

print("filling database")
db = client.cbir_database
doc={str(cluster_index): coord.tolist() for cluster_index, coord in enumerate(centers)}
clusters = db.clusters
clusters.insert_one(doc)
images=db.images
metadata = [
        {
            "cluster": int(predictions[i]),
            "features": features[i, :].tolist(),
            "file_name": files[i]
        } for i in tqdm(range(0,features.shape[0]))]

images.insert_many(metadata)
print("database filled successfully")