import os
import yaml

class DataFlow:
    ID = 'NONE'

    def __init__(self, config, sandbox=False, local_config=False):
        path = os.path.dirname(os.path.abspath(__file__))
        self.sandbox = sandbox
        if not config:
            config = "config.yaml"


        if local_config:
            config_path = config
        else:
            config_path = os.path.join(path, config)

        with open(config_path, 'r') as fp:
            self.config = yaml.safe_load(fp)[self.ID.lower()]
