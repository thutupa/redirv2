from google.appengine.ext import ndb
import webapp2
import webtest
import unittest

from redirect import AddHandler
import redirect
from constants import Constants
import mock
import logic


class AddHandlerTest(unittest.TestCase):
    def setUp(self):
        # Create a WSGI application.
        app = redirect.application
        self.testapp = webtest.TestApp(app)

    # Test something is setup to handle /add
    def testAddHandlerExistsForPost(self):
        response = self.testapp.post(Constants.Paths.ADD_PATH, expect_errors=True)
        self.assertNotEqual(response.status_int, 405)
        self.assertNotEqual(response.status_int, 404)

    # Test that 400 is returned if params are missing.
    def testAddReturns500WhenMissingPhrase(self):
        response = self.testapp.post(Constants.Paths.ADD_PATH, expect_errors=True)
        self.assertEqual(response.status_int, 400)

    # Test that 400 is returned if params are missing.
    def testAddReturns500WhenMissingRedirectLink(self):
        response = self.testapp.post(Constants.Paths.ADD_PATH,
                                     {Constants.Param.PHRASE: 'test phrase'},
                                     expect_errors=True)
        self.assertEqual(response.status_int, 400)

    def testMockCall(self):
        testKey = ndb.Key('Action', 1)
        mockTime = mock.Mock(return_value = testKey)
        with mock.patch('logic.InsertAction', mockTime):
            self.assertTrue(logic.InsertAction('a', 'b') is not None)
        self.assertTrue(mockTime.call_args, (('a', 'b'),))

    def testAddDoesNotInvokeInsertActionWhenParamsAreNotGiven(self):
        testKey = ndb.Key('Action', 1)
        mockTime = mock.Mock(return_value = testKey)
        with mock.patch('logic.InsertAction', mockTime):
            response = self.testapp.post(Constants.Paths.ADD_PATH,
                                         {Constants.Param.PHRASE: 'test phrase'},
                                         expect_errors=True)
            self.assertEqual(response.status_int, 400)
        
        self.assertTrue(mockTime.call_args is None)


    def testAddInvokesInsertActionWhenParamsAreGiven(self):
        TEST_PHRASE = 'test phrase'
        TEST_LINK = 'https://www.facebook.com'
        testKey = ndb.Key('Action', 1)
        mockTime = mock.Mock(return_value = testKey)
        with mock.patch('logic.InsertAction', mockTime):
            response = self.testapp.post(Constants.Paths.ADD_PATH,
                                         {Constants.Param.PHRASE: TEST_PHRASE,
                                          Constants.Param.REDIRECT_LINK: TEST_LINK},
                                         expect_errors=True)
        
        self.assertTrue(mockTime.call_args is not None)
