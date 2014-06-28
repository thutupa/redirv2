import unittest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed
from redirect import Action

class DemoTestCase(unittest.TestCase):

  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()

    self.testbed.init_datastore_v3_stub()


  def tearDown(self):
        self.testbed.deactivate()

  def testInsertEntity(self):
    Action().put()

if __name__ == '__main__':
    unittest.main()
