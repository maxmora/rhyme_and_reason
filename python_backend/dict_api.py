# this provides the server side API code for the searchable dictionary

from bottle import get, route, run
import worddict

DB_FILE = '../db/english_dict.db'
def openDB():
    return worddict.WordDict(DB_FILE)

#@route('/spelling/<sp>', method='GET')
@get('/spelling/<sp>')
def getSpellingWords(sp):
    db = openDB()
    data = db.findSpelling(sp)
    return dict(results=data)

@get('/transcription/<tr>')
def getTranscriptionWords(tr):
    db = openDB()
    data = db.findTranscription(tr)
    return dict(results=data)

@post('/rhyme/<sp>')
def getRhymes(sp):
    db = openDB()
    data = db.findRhymes(sp)
    return dict(results=data)


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
