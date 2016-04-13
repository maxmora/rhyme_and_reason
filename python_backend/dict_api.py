# this provides the server side API code for the searchable dictionary

from bottle import get, post, request, route, run, static_file, template
import worddict

DB_FILE = '../db/english_dict.db'
def openDB():
    return worddict.WordDict(DB_FILE)

# User pages
@get('/search')
def getSearchPage():
    return template('simple_query')

@get('/rhymescheme')
def getSearchPage():
    return template('rhyme_scheme')


# Static resources
# Static resources
@get('/js/<filename:re:.*\.js>') # only css files
def stylesheets(filename):
    return static_file(filename, root='js/')

@get('/css/<filename:re:.*\.css>') # only css files
def stylesheets(filename):
    return static_file(filename, root='css/')


# API routes
@get('/api/spelling/<sp>')
def getSpellingWords(sp):
    db = openDB()
    data = db.findSpelling(sp)
    return dict(results=data)

@get('/api/transcription/<tr>')
def getTranscriptionWords(tr):
    db = openDB()
    data = db.findTranscription(tr)
    return dict(results=data)

@get('/api/rhyme/<sp>')
def getRhymes(sp):
    db = openDB()
    data = db.findRhymes(sp)
    return dict(results=data)

@post('/api/rhymescheme')
def getRhymeScheme():
    poem_text = request.json.get('poem_text')
    db = openDB()
    t = worddict.Text(poem_text,db)
    data = t.getRhymeSchemeAnnotatedLines()
    return dict(annotations=data)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)

