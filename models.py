from google.appengine.ext import ndb

def GetAccountKey(userId):
    return ndb.Key('Account', userId)

MAX_NUM_KEYWORDS = 10
class Action(ndb.Model):
    keywords = ndb.StringProperty(repeated=True)
    redirect_link = ndb.StringProperty(indexed=False)
