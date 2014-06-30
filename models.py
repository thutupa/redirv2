from google.appengine.ext import ndb

class Action(ndb.Model):
    keywords = ndb.StringProperty(repeated=True)
    redirect_link = ndb.StringProperty(indexed=False)
