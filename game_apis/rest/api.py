import os
import yaml

class API:
    ID = 'NONE'

    def __init__(self, config, sandbox=False, local_config=False):
        path = os.path.dirname(os.path.abspath(__file__))
        self.key_id, self.key_secret, self.key_passphrase = None, None, None
        self.sandbox = sandbox
        if not config:
            config = "config.yaml"

        try:
            if local_config:
                config_path = config
            else:
                config_path = os.path.join(path, config)

            with open(config_path, 'r') as fp:
                data = yaml.safe_load(fp)
                self.key_id = data[self.ID.lower()]['key_id']
                if 'key_secret' in data[self.ID.lower()]
                    self.key_secret = data[self.ID.lower()]['key_secret']
                if 'key_passphrase' in data[self.ID.lower()]:
                    self.key_passphrase = data[self.ID.lower()]['key_passphrase']
        except (KeyError, FileNotFoundError, TypeError):
            pass
