import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from redirect import Action

class ActionTestCase(unittest.TestCase):

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

  def testFetchRedirectAttribute(self):
    TEST_PHRASE = 'test phrase'
    act = Action(redirect_link=TEST_PHRASE)
    act.put()

    self.assertEquals(1, len(Action.query().fetch(2)))
    fetched = Action.query().fetch(2)[0]
    self.assertEquals(TEST_PHRASE, fetched.redirect_link)

if __name__ == '__main__':
    unittest.main()
