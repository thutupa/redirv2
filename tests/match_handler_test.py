from google.appengine.ext import ndb
from google.appengine.ext import testbed
import webapp2
import webtest
import unittest
import urlparse

from redirect import AddHandler
import redirect
from constants import Constants
import mock
import logic
import models

class MatchHandlerTest(unittest.TestCase):
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

    # Test something is setup to handle /match
    def testMatchHandlerExistsForPost(self):
        response = self.testapp.post(Constants.Path.MATCH_PATH, expect_errors=True)
        self.assertNotEqual(404, response.status_int)
        self.assertNotEqual(405, response.status_int)
    
    def testMatchHandlerReturns400WithNoParam(self):
        response = self.testapp.post(Constants.Path.MATCH_PATH, expect_errors=True)
        print response.status_int
        self.assertEqual(400, response.status_int)
    
