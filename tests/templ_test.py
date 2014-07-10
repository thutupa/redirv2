import unittest
import templ
import datetime
from models import Action

class FakeAction(object):
    def __init__(self, id, keywords, link):
        self._id = id
        self.keywords = keywords
        self._link = link
        # Use a fixed date for testability
        self.created = datetime.datetime.fromtimestamp(1405021513)
        
    def getKeywordsAsPharse(self):
        return ' '.join(sorted(self.keywords))
    
    def key(self):
        return self

    def urlsafe(self):
        return self.id()

    def id(self):
        return self._id

class RedirectHandlerTest(unittest.TestCase):
    def setUp(self): pass

    def tearDown(self): pass

    def testInsertTemplateReturnsSomething(self):
        self.assertTrue(')];{id: \'testId\'}', templ.InsertResultJson('testId'))

    def testMatchTemplateOnEmpty(self):
        self.assertEqual(')];[\n[]', templ.MatchResultJson(actions=[]))

    def testMatchTemplateOnSingle(self):
        actions = [FakeAction(1, ['a', 'b'], 'https://www.google.com')]
        self.assertEqual(")];[\n[\n{id: '1', phrase: 'a b', link: ''}, created, :'2014-07-10'\n]", templ.MatchResultJson(actions=actions))
