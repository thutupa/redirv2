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
        response = self.testapp.get(Constants.Path.REDIRECT_PATH, expect_errors=True)
        self.assertNotEqual(response.status_int, 405)
        self.assertNotEqual(response.status_int, 404)

    # Test that it return 400 when match param is not given
    def testRedirectHandlerReturns400WithNoParam(self):
        response = self.testapp.get(Constants.Path.REDIRECT_PATH, expect_errors=True)
        self.assertEqual(response.status_int, 400)

    # Test that it invokes SearchAction when match param is given.
    def testRedirectInvokesSearchActionWithParam(self):
        TEST_LINK = 'https://www.facebook.com'
        mockSearchAction = mock.Mock(return_value = [models.Action(redirect_link=TEST_LINK)])
        with mock.patch('logic.SearchAction', mockSearchAction):
            response = self.testapp.get(Constants.Path.REDIRECT_PATH,
                                        {Constants.Param.MATCH: 'test phrase'},
                                        expect_errors=True)
            self.assertEqual(302, response.status_int)
            self.assertEqual(TEST_LINK, response.headers['Location'])

    # Test that it invokes SearchAction when match param is given.
    def testRedirectWithMoreThanOneMatch(self):
        TEST_LINK = 'https://www.facebook.com'
        TEST_LINK2 = 'https://www.facebook.com1'
        mockSearchAction = mock.Mock(return_value = [models.Action(redirect_link=TEST_LINK),
                                                     models.Action(redirect_link=TEST_LINK2)])
        with mock.patch('logic.SearchAction', mockSearchAction):
            response = self.testapp.get(Constants.Path.REDIRECT_PATH,
                                        {Constants.Param.MATCH: 'test phrase'},
                                        expect_errors=True)
            self.assertEqual(302, response.status_int)
            urlp = urlparse.urlparse(response.headers['Location'])
            self.assertEqual(Constants.Path.MAIN_PATH, urlp.path)
