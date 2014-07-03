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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        raise Exception('Not implemented')

class MatchHandler(webapp2.RequestHandler):
    def get(self):
        raise Exception('Not implemented')

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
        id = self.request.get(Constants.Param.ID, '')
        if id:
            actionKey = logic.UpdateAction(user.user_id(), id, phrase, redirect_link)
        else:
            actionKey = logic.InsertAction(user.user_id(), phrase, redirect_link)
        template = JINJA_ENVIRONMENT.get_template('insert.json')
        self.response.write(template.render({'id': actionKey.id()}))


class RedirectHandler(webapp2.RequestHandler):
    def get(self):
        match = self.request.get(Constants.Param.MATCH, '')
        if not match:
            self.response.set_status(400)
            return
        actions = logic.SearchAction(match)
        if len(actions) == 1:
            return self.redirect(actions[0].redirect_link)
        return self.redirect(Constants.Path.MAIN_PATH + '?' + Constants.Param.MATCH + '=' + match)
        

application = webapp2.WSGIApplication([
    (Constants.Path.MAIN_PATH, MainHandler),
    (Constants.Path.MATCH_PATH, MatchHandler),
    (Constants.Path.ADD_PATH, AddHandler),
    (Constants.Path.REDIRECT_PATH, RedirectHandler),
], debug=True)
