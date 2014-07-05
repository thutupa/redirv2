from google.appengine.api import users

import jinja2
import webapp2
import os

from constants import Constants
import logic
import templ

class MainHandler(webapp2.RequestHandler):
    def get(self):
        return self.response.write(templ.MainResultHtml())

class MatchHandler(webapp2.RequestHandler):
    def get(self):
        match = self.request.get(Constants.Param.MATCH, '')
        if not match:
            self.response.set_status(400)
            return
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        actions = logic.SearchAction(user.user_id(), match)
        return self.response.write(templ.MatchResultJson(actions))


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
        self.response.write(templ.InsertResultJson(actionId=str(actionKey.id())))


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
