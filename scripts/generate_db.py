#!/bin/env python3

# parse file and migrate data into an SQLite database file

import parse
import sqlite3

def generate_db(db_name,word_data):
    conn = sqlite3.connect(db_name)

    c = conn.cursor()

    c.execute('CREATE TABLE words(spelling varchar(50), transcription varchar(50), stress varchar(50));')

    for i in word_data:
        db_entry = (i['spelling'],i['transcription'],i['stress'])
        c.execute('INSERT INTO words VALUES (?,?,?)', db_entry)

    conn.commit()
    conn.close()

parsed = parse.generate_word_list_from_file('../../cmudict.0.7a')
generate_db('english_dict.db',parsed)

def find_by_spelling(data_list,spelling):
    '''Search for 'spelling' in a parsed data_list. Intended only for
       interactive use.'''
    results = []
    for entry in data_list:
        if entry['spelling'] == spelling:
            results.append(entry)
    if len(results) == 0:
        results = None
    return results
