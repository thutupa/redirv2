import webapp2
import webtest
import unittest

from redirect import AddHandler
from constants import Constants

class AddHandlerTest(unittest.TestCase):
    def setUp(self):
        # Create a WSGI application.
        app = webapp2.WSGIApplication([(Constants.Paths.ADD_PATH, AddHandler)])
        self.testapp = webtest.TestApp(app)

    # Test the handler.
    def testAddHandlerReturnErrorWhenCalledWithNoParams(self):
        response = self.testapp.get(Constants.Paths.ADD_PATH)
        self.assertEqual(response.status_int, 500)
