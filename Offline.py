from utilis import PretrainedModel
from mlinsights.mlmodel import KMeansL1L2
from MongoEngine import MongoConnector
from tqdm import tqdm
import numpy as np
import os


def extract_clusters(source_dir, model):
    files = os.listdir(source_dir)
    files_paths = [os.path.join(dirs, file) for file in files]
    features = np.array([model.extract_features(file) for file in tqdm(files_paths)]).squeeze()
    kml1 = KMeansL1L2(5, norm='L1')
    kml1.fit(features)
    centers = kml1.cluster_centers_
    predictions = kml1.predict(features)
    return centers, predictions, features ,files

if __name__== "__main__":
    model = PretrainedModel()
    dirs = "static/photos"
    centers, predictions, features,files = extract_clusters(dirs,model)
    db_connector = MongoConnector("localhost", "cbir_database")
    print("filling database")
    doc = {str(cluster_index): coord.tolist() for cluster_index, coord in enumerate(centers)}
    clusters = db_connector.get_collection("clusters")
    db_connector.insert_doc(clusters, doc)
    images = db_connector.get_collection("images")
    metadata = [
            {
                "cluster": int(predictions[i]),
                "features": features[i, :].tolist(),
                "file_name": files[i]
            } for i in tqdm(range(0, features.shape[0]))]

    db_connector.insert_docs(images, metadata)
    print("database filled successfully")