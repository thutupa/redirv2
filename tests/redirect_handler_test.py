from google.appengine.ext import ndb
from google.appengine.ext import testbed
import webapp2
import webtest
import unittest

from redirect import AddHandler
import redirect
from constants import Constants
import mock
import logic


class RedirectHandlerTest(unittest.TestCase):
    def setUp(self):
        # Create a WSGI application.
        app = redirect.application
        self.testapp = webtest.TestApp(app)
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()

    def tearDown(self):
        self.testbed.deactivate()

    # Test something is setup to handle /redirect
    def testRedirectHandlerExistsForGet(self):
        response = self.testapp.get(Constants.Paths.REDIRECT_PATH, expect_errors=True)
        self.assertNotEqual(response.status_int, 405)
        self.assertNotEqual(response.status_int, 404)

    # Test that it return 400 when match param is not given
    def testRedirectHandlerReturns400WithNoParam(self):
        response = self.testapp.get(Constants.Paths.REDIRECT_PATH, expect_errors=True)
        self.assertEqual(response.status_int, 400)
