import unittest
from google.appengine.ext import testbed
from models import GetAccountKey
from models import Action
from logic import InsertAction
from logic import UpdateAction
from logic import DeleteAction

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

  def testUpdateAction(self):
    TEST_USER_ID = 'testUserId'
    TEST_PHRASE = 'this is a test'
    TEST_LINK = 'https://www.google.com/shopping/express'
    
    actionKey = InsertAction(TEST_USER_ID, TEST_PHRASE, TEST_LINK)
    TEST_LINK_2 = 'https://www.google.com'
    UpdateAction(actionKey, TEST_PHRASE, TEST_LINK_2)
    fetched = actionKey.get()
    self.assertEquals(fetched.redirect_link, TEST_LINK_2)

  def testUpdatePhrase(self):
    TEST_USER_ID = 'testUserId'
    TEST_PHRASE = 'this is a test'
    TEST_LINK = 'https://www.google.com/shopping/express'
    
    actionKey = InsertAction(TEST_USER_ID, TEST_PHRASE, TEST_LINK)
    TEST_PHRASE_2 = 'marky mark is whalberg'
    UpdateAction(actionKey, TEST_PHRASE_2, TEST_LINK)
    fetched = actionKey.get()
    for word in TEST_PHRASE_2.split(' '):
      self.assertTrue(word in fetched.keywords)

  def testDeleteAction(self):
    TEST_USER_ID = 'testUserId'
    TEST_PHRASE = 'this is a test'
    TEST_LINK = 'https://www.google.com/shopping/express'
    
    accountKey = GetAccountKey(TEST_USER_ID)
    actionKey = InsertAction(TEST_USER_ID, TEST_PHRASE, TEST_LINK)
    DeleteAction(actionKey)
    self.assertEquals(0, len(Action.query(ancestor=accountKey).fetch(2)))