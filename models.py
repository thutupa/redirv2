from google.appengine.ext import ndb

def GetAccountKey(userId): pass

MAX_NUM_KEYWORDS = 10
class Action(ndb.Model):
    keywords = ndb.StringProperty(repeated=True)
    redirect_link = ndb.StringProperty(indexed=False)
    
    def setKeywordsFromPhrase(self, phrase):
        # extra split to ignore
        words = phrase.split(' ', MAX_NUM_KEYWORDS + 1)
        words = [word.lower() for word in words[:MAX_NUM_KEYWORDS]]
        self.keywords = words
