from google.appengine.api import users

import jinja2
import webapp2
import os

from constants import Constants

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler): pass

class AddHandler(webapp2.RequestHandler):
    def post(self):
        phrase = self.request.get(Constants.Param.PHRASE, '')
        redirect_link = self.request.get(Constants.Param.REDIRECT_LINK, '')
        if not phrase or not redirect_link:
            self.response.set_status(400)
            return
        raise Exception('Not implemented')
    

application = webapp2.WSGIApplication([
    ('/', MainPage),
    (Constants.Paths.ADD_PATH, AddHandler),
], debug=True)
