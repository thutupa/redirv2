import unittest
import templ

class RedirectHandlerTest(unittest.TestCase):
    def setUp(self): pass

    def tearDown(self): pass

    def testInsertTemplateReturnsSomething(self):
        self.assertTrue(')];{id: \'testId\'}', templ.InsertJson('testId'))

    def testMatchTemplate(self):
        self.assertTrue(')];[]', templ.MatchResultJson(actions=[]))
