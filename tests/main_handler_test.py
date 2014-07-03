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

class MainHandlerTest(unittest.TestCase):
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

    
