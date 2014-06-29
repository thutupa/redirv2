from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Action(ndb.Model):
    phrase = ndb.StringProperty(indexed=False)
    redirect_link = ndb.StringProperty(indexed=False)

class MainPage(webapp2.RequestHandler): pass

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
