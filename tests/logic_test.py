import unittest
from google.appengine.ext import testbed
from logic import InsertAction
from models import GetAccountKey
from models import Action

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

  def testInsertAction(self):
    TEST_USER_ID = 'testUserId'
    TEST_PHRASE = 'this is a test'
    TEST_LINK = 'https://www.google.com/shopping/express'
    
    InsertAction(TEST_USER_ID, TEST_PHRASE, TEST_LINK)

    accountKey = GetAccountKey(TEST_USER_ID)
    self.assertEquals(1, len(Action.query(ancestor=accountKey).fetch(2)))
    fetched = Action.query().fetch(2)[0]
    self.assertEquals(fetched.redirect_link, TEST_LINK)

  def testInsertActionReturnsKey(self):
    TEST_USER_ID = 'testUserId'
    TEST_PHRASE = 'this is a test'
    TEST_LINK = 'https://www.google.com/shopping/express'
    
    actionKey = InsertAction(TEST_USER_ID, TEST_PHRASE, TEST_LINK)

    fetched = actionKey.get()
    self.assertEquals(fetched.redirect_link, TEST_LINK)
