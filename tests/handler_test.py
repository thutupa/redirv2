import webapp2
import webtest
import unittest

from redirect import AddHandler
import redirect
from constants import Constants

class AddHandlerTest(unittest.TestCase):
    def setUp(self):
        # Create a WSGI application.
        app = redirect.application
        self.testapp = webtest.TestApp(app)

    # Test the handler.
    def testAddHandlerReturnErrorWhenCalledWithNoParams(self):
        response = self.testapp.post(Constants.Paths.ADD_PATH)
        self.assertEqual(response.status_int, 500)
