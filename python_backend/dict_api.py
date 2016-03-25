# this provides the server side API code for the searchable dictionary

from flask import Flask, jsonify, request
import worddict

app = Flask(__name__)

DB_FILE = '../db/english_dict.db'
def openDB():
    return worddict.WordDict(DB_FILE)

@app.route('/spelling/<string:sp>', methods=['GET'])
def getSpellingWords(sp):
    db = openDB()
    data = db.findSpelling(sp)
    return jsonify(results=data)

@app.route('/transcription/<string:tr>', methods=['GET'])
def getTranscriptionWords(tr):
    db = openDB()
    data = db.findTranscription(tr)
    return jsonify(results=data)

@app.route('/rhyme/<string:sp>', methods=['GET'])
def getRhymes(sp):
    db = openDB()
    data = db.findRhymes(sp)
    return jsonify(results=data)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
    #app.run(host='0.0.0.0',port=31337)
