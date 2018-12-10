from game_apis.data_flow import DataFlow
from azure.storage.blob import BlockBlobService
from io import StringIO
import yaml
import json


class AzureBlobFlow(DataFlow):
    ID = 'AZUREBLOB_CREDS'

    def __init__(self, config, sandbox=False, local_config=False):
        super().__init__(config, sandbox, local_config)

        self.account_name = self.config['account_name']
        self.account_key = self.config['account_key']
        self.container = self.config['container']

        self.init_service()

    def init_service(self):
        block_blob_service = BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key
        )

        self.blob_service = block_blob_service

        return self.blob_service


    def write(self, object, file_name):

        obj_string = json.dumps(object)

        msg = self.blob_service.create_blob_from_text(
            self.container,
            file_name,
            obj_string
        )

        return msg
