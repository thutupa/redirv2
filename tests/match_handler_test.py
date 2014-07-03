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
        self.assertEqual(400, response.status_int)
    
    def testsMatchHandlerRedirectWithoutUser(self):
        TEST_LINK = 'https://www.facebook.com'
        mockSearchAction = mock.Mock(return_value = [models.Action(redirect_link=TEST_LINK)])
        with mock.patch('logic.SearchAction', mockSearchAction):
            response = self.testapp.get(Constants.Path.MATCH_PATH,
                                        {Constants.Param.MATCH: 'test phrase'},
                                        expect_errors=True)

        self.assertEqual(302, response.status_int)
