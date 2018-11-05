import unittest

import rest
from rest import rest
from rest.rest import Rest

class TestRiot(unittest.TestCase):

    def test_hello_world(self):
        riot = Rest('config.yaml').Riot
        hello = riot.hello_world()

        assert hello['id'] == 585897



if __name__ == '__main__':
    unittest.main()
