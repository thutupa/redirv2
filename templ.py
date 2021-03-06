import os
import jinja2
import constants

def templateDir():
    return os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templateDir()),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

JINJA_ENVIRONMENT.globals['Constants'] = constants.Constants

# TODO(syam): Could this lookup be cached?
def lookupTemplate(fname):
    return JINJA_ENVIRONMENT.get_template(fname)

def InsertResultJson(actionId=''):
    templ = lookupTemplate('insert.json')
    return _renderTemplate(templ, {'id': actionId})

def MatchResultJson(actions=[]):
    templ = lookupTemplate('match.json')
    return _renderTemplate(templ, {'actions': actions})

def _renderTemplate(templ, params):
    return templ.render(params)

def MainResultHtml():
    return _renderTemplate(lookupTemplate('main.html'), {})
