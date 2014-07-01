from google.appengine.api import users

import jinja2
import webapp2
import os

from constants import Constants
import logic

def templateDir():
    return os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templateDir()),
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
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        insertedKey = logic.InsertAction(user.user_id(), phrase, redirect_link)
        template = JINJA_ENVIRONMENT.get_template('insert.json')
        self.response.write(template.render({'id': insertedKey.id()}))

    

application = webapp2.WSGIApplication([
    ('/', MainPage),
    (Constants.Paths.ADD_PATH, AddHandler),
], debug=True)
