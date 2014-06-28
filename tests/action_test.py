import unittest
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
    self.testbed.init_memcache_stub()


  def tearDown(self):
        self.testbed.deactivate()

  def testInsertEntity(self):
    act = Action()
    act.phrase = 'test phrase'
    act.put()

    self.assertEquals(1, len(Action.query().fetch(2)))

if __name__ == '__main__':
    unittest.main()
