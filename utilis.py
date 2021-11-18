from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img
import numpy as np


class PretrainedModel:
    def __init__(self, database=None, weights="imagenet", input_shape=(120, 120, 3)):
        pretrained_model = ResNet50(weights=weights, input_tensor=Input(shape=input_shape))
        self.model = Model(inputs=pretrained_model.inputs, outputs=pretrained_model.layers[-2].output)
        self.db = database

    @staticmethod
    def l1_distance(a, b):
        return np.sum(np.abs(a-b))

    def extract_features(self, image):
        image = load_img(image, target_size=(120, 120))
        # convert the image pixels to a numpy array
        image = img_to_array(image)
        # reshape data for the model
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        # prepare the image for the VGG model
        image = preprocess_input(image)
        output = np.array(self.model.predict(image)).flatten()
        return output

    def get_images(self, image, nsi=20):
        features = self.extract_features(image)
        clusters = self.db.clusters.find_one()
        clusters.pop("_id")
        distances = np.array([self.l1_distance(cluster, features) for cluster in clusters.values()])
        cluster_index = int(np.argmin(distances))
        images = self.db.images.find({"cluster": cluster_index})
        files = {image["file_name"] : self.l1_distance(np.array(list(clusters.values())[cluster_index]),\
                                                       np.array(image["features"])) for image in images}
        sorted_files = {k: v for k, v in sorted(files.items(), key=lambda item: item[1])}  # sorting dict by value
        keys=list(sorted_files.keys())
        output = [keys[i] for i in range(nsi)]
        return output
