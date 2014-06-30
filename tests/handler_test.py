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

    # Test something is setup to handle
    def testAddHandlerExistsForPost(self):
        response = self.testapp.post(Constants.Paths.ADD_PATH, expect_errors=True)
        self.assertNotEqual(response.status_int, 405)
        self.assertNotEqual(response.status_int, 404)
