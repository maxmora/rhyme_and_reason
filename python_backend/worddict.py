# Provides the WordDict class as a database abstraction for accessing pronunciation data
import sqlite3

class WordDict:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.conn_cursor = self.connection.cursor()

    def rowAsDict(self,row):
        d = {}
        for idx, col in enumerate(self.conn_cursor.description):
            d[col[0]] = row[idx]
        return d

    def findSpelling(self,sp):
        sp = sp.upper()
        spelling_tuple = (sp,)
        results = self.conn_cursor.execute("SELECT * FROM words WHERE spelling=?;",spelling_tuple)
        #return [r for r in results]
        return [self.rowAsDict(r) for r in results]

    def findTranscription(self,tr):
        trans_tuple = (tr,)
        results = self.conn_cursor.execute("SELECT * FROM words WHERE transcription=?;",trans_tuple)
        return [self.rowAsDict(r) for r in results]

    # TODO this should check that the RESULTS have the primary stress in the right place, or else e.g.,
    # "tree" would rhyme with "pretty" and such.
    def findRhymes(self,sp):
        all_results = []
        trans = Transcriptions()
        for w in self.findSpelling(sp):
            rhyme_segs = trans.getRhyme(w['transcription'],w['stress'])
            query_tuple = ('*' + rhyme_segs,w['spelling'])
            rhyme_seg_matches = self.conn_cursor.execute("SELECT * FROM words WHERE transcription GLOB ? AND spelling != ?;", query_tuple)
            # only keeps results if the rhyme in the match actually has main stress on the first vowel
            results = [rh for rh in rhyme_seg_matches if trans.isRhymeMainStressed(rhyme_segs,self.rowAsDict(rh))]

            all_results.extend(results)
        return [self.rowAsDict(r) for r in all_results]

class Transcriptions:
    hammond_vowels = ['a', '@', 'x', 'c', 'W', 'Y', 'E', 'R', 'e', 'I', 'i', 'o', 'O', 'U', 'u']

    def getMainStressIndex(self,stress):
        '''Get the index of the main stress '1' in the stress string. This is equivalent to the
           main stressed syllable (Nth-1).'''
        i = 0
        for s in stress:
            if s == '1':
                return i
            i += 1
        return None

    def getNthVowelIndex(self,transcription,syl_num):
        '''Return the index of the N-1th (that is, syl_num) vowel in the transcription string.'''
        i = 0
        syl = 0
        for c in transcription:
            if c in self.hammond_vowels:
                if syl == syl_num:
                    return i
                syl += 1
            i += 1
        
    def getRhyme(self,transcription,stress):
        '''Return the segments that make the up the rhyme of the word (all segments from main
           stress onwards.'''
        main_stress_i = self.getMainStressIndex(stress)
        start_of_rhyme = self.getNthVowelIndex(transcription,main_stress_i)
        return transcription[start_of_rhyme:]

    def isRhymeMainStressed(self,rhyme,test_word_dict):
        '''Take a rhyme and a dict representation of a test word entry and return True if the first
           vowel of the rhyme is main stressed in the test word, otherwise return False.'''
        # count vowels in rhyme string
        rhyme_vowel_count = len([c for c in rhyme if c in self.hammond_vowels])
        # if that number of vowels back in the stress string is main stress, then rhyme started
        # with main stress
        if test_word_dict['stress'][-rhyme_vowel_count] == '1':
            return True
        else:
            return False

