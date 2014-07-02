from google.appengine.ext import ndb
from models import Action
from models import GetAccountKey

def InsertAction(userId, phrase, link):
    act = Action(parent=GetAccountKey(userId))
    act.setKeywordsFromPhrase(phrase)
    act.redirect_link = link
    return act.put()

def UpdateAction(userId, actionId, newPhrase, newLink):
    actionKeyPairs = GetAccountKey(userId).pairs() + (('Action', actionId),) 
    act = ndb.Key(pairs=actionKeyPairs).get()
    act.setKeywordsFromPhrase(newPhrase)
    act.redirect_link = newLink
    return act.put()

def DeleteAction(key):
    key.delete()

def SearchAction(keywords):
    raise Exception('Not Implemented')

def SplitPhrase(phrase):
    raise Exception('Not Implemented')
