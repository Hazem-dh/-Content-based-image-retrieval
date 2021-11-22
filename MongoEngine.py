from pymongo import MongoClient
import logging
import sys

logging.basicConfig(format='%(levelname)s-%(asctime)s : %(message)s', level=logging.INFO)


class MongoConnector:
    """ database connector class """

    def __init__(self, server, db_name):
        self.server = server
        self.database_name = db_name
        try:
            client = MongoClient(self.server)
        except Exception:
            logging.error("DATABASE IN NOT OPEN , PLEASE LAUNCH MONGODB AND RETRY")
            sys.exit(1)
        self.database = client[self.database_name]

    def get_collection(self, collection_name):
        """return the collection the """
        collection = self.database[collection_name]
        return collection

    @staticmethod
    def insert_doc(collection, post):
        collection.insert_one(post)
        logging.info("Data successfully inserted")

    @staticmethod
    def insert_docs(collection, post):
        collection.insert_many(post)
        logging.info("Data successfully inserted")
