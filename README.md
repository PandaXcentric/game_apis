# game_apis
This repository is for integrating with different apis to allow you to pull player or game data

# Install
To install the api so it's importable do:<br />
```sudo python3 setup.py install```<br /><br />
Once it's installed you can do<br />
```from game_apis.rest import Rest```

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
riot = Rest('config.yaml').Riot
hello = riot.hello_world()
```
