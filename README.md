# game_apis
This repository is for integrating with different apis to allow you to pull player or game data

# Install
To install the api so it's importable do:<br />
```sudo python3 setup.py install```<br /><br />
Once it's installed you can do<br />
```from game_apis.rest import Rest```

# Config
To use some of the REST Apis you need your keys in the config.yaml file. The config file should be in the rest directory.<br />
Here's an example of the Rest Config:<br />
```
opendota:
  key_id: null
riot:
  key_id: null
pubg:
  key_id: null
egb:
  key_id: null
  key_secret: null
riotesports:
  key_id: null
fortnitetracker:
  key_id: null
  ```
<br />

  A good way to see what should be in the config is by looking at the base class that loads the config file and seeing what keys it expects. Normally it'll look for the ID of the child class, which is a field on that child class, and then have the parameters that class needs as children of it in the confg. <br />

  The same thing is true for data_flow. You have the ID of the class lowercased (ID = 'AZUREBLOB_CREDS') and then as children of that in the config the fields it uses, for example self.config['account_name']. In this case you'd want:
```
  azureblob_creds:
    account_name: null
 ```
 <br />

# Run tests
To run all unit tests in a file do:<br />
```python3 -m unittest test.rest.test_open_dota```

To run a specific unit test do:<br />
```python3 -m unittest test.rest.test_open_dota.TestOpenDota.test_get_lane_roles```

# Using API
Initialize the rest class with<br />
```api = Rest('<path to config.yaml>')```

You can find the implemented apis with<br />
```api.lookup```

An example usage of this repo is
```
from game_apis.rest import Rest

riot = Rest('config.yaml').Riot
hello = riot.hello_world()
```
