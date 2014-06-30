from models import Action
from models import GetAccountKey

def InsertAction(userId, phrase, link):
    act = Action(parent=GetAccountKey(userId))
    act.setKeywordsFromPhrase(phrase)
    act.redirect_link = link
    return act.put()
