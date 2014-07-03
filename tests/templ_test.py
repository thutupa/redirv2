import unittest
import templ

class RedirectHandlerTest(unittest.TestCase):
    def setUp(self): pass

    def tearDown(self): pass

    # Test something is setup to handle /redirect
    def testInsertTemplateReturnsSomething(self):
        self.assertTrue(')];{id: \'testId\'}', templ.InsertJson('testId'))
