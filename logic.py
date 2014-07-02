from google.appengine.ext import ndb
from models import Action
from models import GetAccountKey

def InsertAction(userId, phrase, link):
    act = Action(parent=GetAccountKey(userId))
    act.keywords = SplitPhrase(phrase)
    act.redirect_link = link
    return act.put()

def UpdateAction(userId, actionId, newPhrase, newLink):
    actionKeyPairs = GetAccountKey(userId).pairs() + (('Action', actionId),) 
    act = ndb.Key(pairs=actionKeyPairs).get()
    act.keywords = SplitPhrase(newPhrase)
    act.redirect_link = newLink
    return act.put()

def DeleteAction(key):
    key.delete()

def SearchAction(phrase):
    return []

# temporary import of MAX_NUM_KEYWORDS
from models import MAX_NUM_KEYWORDS
def SplitPhrase(phrase):
    # extra split to ignore extra words
    words = phrase.split(' ', MAX_NUM_KEYWORDS)
    return [word.lower() for word in words[:MAX_NUM_KEYWORDS]]

