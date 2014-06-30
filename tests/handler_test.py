import webapp2
import webtest
import unittest

from redirect import AddHandler

class AddHandlerTest(unittest.TestCase):
    def setUp(self):
        # Create a WSGI application.
        app = webapp2.WSGIApplication([('/add', AddHandler)])
        self.testapp = webtest.TestApp(app)

    # Test the handler.
    def testAddHandlerReturnErrorWhenCalledWithNoParams(self):
        response = self.testapp.get('/add')
        self.assertEqual(response.status_int, 500)
