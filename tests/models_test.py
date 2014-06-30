import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from models import Action
from models import MAX_NUM_KEYWORDS
from models import GetAccountKey
from models import InsertAction

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
    TEST_LINK = 'test link'
    act = Action(redirect_link=TEST_LINK)
    act.put()

    self.assertEquals(1, len(Action.query().fetch(2)))
    fetched = Action.query().fetch(2)[0]
    self.assertEquals(TEST_LINK, fetched.redirect_link)

  def testFetchKeywordsAttribute(self):
    TEST_KEY_WORDS = ['key', 'words', 'test']
    act = Action(keywords=TEST_KEY_WORDS)
    act.put()

    self.assertEquals(1, len(Action.query().fetch(2)))
    fetched = Action.query().fetch(2)[0]
    for word in TEST_KEY_WORDS:
      self.assertTrue(word in fetched.keywords)

  def testKeyphraseSplitsWords(self):
    TEST_KEY_WORDS = ['key', 'words', 'test']
    keyPhrase = ' '.join(TEST_KEY_WORDS)
    act = Action()
    act.setKeywordsFromPhrase(keyPhrase)
    act.put()

    self.assertEquals(1, len(Action.query().fetch(2)))
    fetched = Action.query().fetch(2)[0]
    for word in TEST_KEY_WORDS:
      self.assertTrue(word in fetched.keywords)

  def testKeyphraseLowerCasesWords(self):
    TEST_KEY_WORDS = ['key', 'words', 'test']
    TEST_KEY_WORDS_NON_LOWER = ['KEY', 'Words', 'tEst']
    keyPhrase = ' '.join(TEST_KEY_WORDS_NON_LOWER)
    act = Action()
    act.setKeywordsFromPhrase(keyPhrase)
    act.put()

    self.assertEquals(1, len(Action.query().fetch(2)))
    fetched = Action.query().fetch(2)[0]
    for word in TEST_KEY_WORDS:
      self.assertTrue(word in fetched.keywords)

  def testKeyphraseAcceptsMax(self):
    TEST_KEY_WORDS = [str(i) for i in range(MAX_NUM_KEYWORDS + 100)]
    keyPhrase = ' '.join(TEST_KEY_WORDS)
    act = Action()
    act.setKeywordsFromPhrase(keyPhrase)
    act.put()

    self.assertEquals(1, len(Action.query().fetch(2)))
    fetched = Action.query().fetch(2)[0]
    for word in TEST_KEY_WORDS[:MAX_NUM_KEYWORDS]:
      self.assertTrue(word in fetched.keywords)
    for word in TEST_KEY_WORDS[MAX_NUM_KEYWORDS:]:
      self.assertTrue(word not in fetched.keywords)

  def testGetAccountKey(self):
    TEST_USER_ID = 'testUserId'
    accountKey = GetAccountKey(TEST_USER_ID)
    self.assertEquals(accountKey.id(), TEST_USER_ID)

  def testInsertWithAccountKey(self):
    TEST_USER_ID = 'testUserId'
    accountKey = GetAccountKey(TEST_USER_ID)
    act = Action(parent=accountKey)
    act.setKeywordsFromPhrase('a b c')
    act.put()

    self.assertEquals(1, len(Action.query(ancestor=accountKey).fetch(2)))

  def testInsertAction(self):
    TEST_USER_ID = 'testUserId'
    TEST_PHRASE = 'this is a test'
    TEST_LINK = 'https://www.google.com/shopping/express'
    
    InsertAction(TEST_USER_ID, TEST_PHRASE, TEST_LINK)

    accountKey = GetAccountKey(TEST_USER_ID)
    self.assertEquals(1, len(Action.query(ancestor=accountKey).fetch(2)))
    fetched = Action.query().fetch(2)[0]
    self.assertEquals(fetched.redirect_link, TEST_LINK)

if __name__ == '__main__':
    unittest.main()
