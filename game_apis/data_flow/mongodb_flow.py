from game_apis.data_flow import DataFlow
import pymongo
import yaml

class MongoDBFlow(DataFlow):
    ID = 'MONGODB_CREDS'

    def __init__(self, config, sandbox=False, local_config=False):
        super().__init__(config, sandbox, local_config)

        self.db_user = self.config['db_user']
        self.db_pass = self.config['db_pass']
        self.db_server = self.config['db_server']
        self.db_name = self.config['db_name']
        self.collection_name = self.config['collection_name']

        self.collection = init_collection()

    def init_collection():
        uri = "mongodb://{0}:{1}@{2}/?ssl=true&replicaSet=globaldb".format(
            self.db_user,
            self.db_pass,
            self.db_server
        )

        client = pymongo.MongoClient(uri)
        db = client[self.db_name]

        return db[self.collection_name]


    def load(self, document):
        return self.collection.insert_one(document)
