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
            rhyme_seg_matches = self.conn_cursor.execute("SELECT * FROM words WHERE transcription GLOB ? AND spelling != ?;",query_tuple)
            # only keeps results if the rhyme in the match actually has main stress on the first vowel
            results = [rh for rh in rhyme_seg_matches if trans.isRhymeMainStressed(rhyme_segs,self.rowAsDict(rh))]

            all_results.extend(results)
        return [self.rowAsDict(r) for r in all_results]

class Transcriptions:
    hammond_vowels = ['a', '@', 'x', 'c', 'W', 'Y', 'E', 'R', 'e', 'I', 'i', 'o', 'O', 'U', 'u']

    def _getMainStressIndex(self,stress):
        '''Get the index of the main stress '1' in the stress string. This is equivalent to the
           main stressed syllable (Nth-1).'''
        i = 0
        for s in stress:
            if s == '1':
                return i
            i += 1
        return None

    def _getNthVowelIndex(self,transcription,syl_num):
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
        main_stress_i = self._getMainStressIndex(stress)
        start_of_rhyme = self._getNthVowelIndex(transcription,main_stress_i)
        return transcription[start_of_rhyme:]

    def isRhymeMainStressed(self,rhyme,test_word_dict):
        '''Take a rhyme and a dict representation of a test word entry and return True if the first
           vowel of the rhyme is main stressed in the test word, otherwise return False.'''
        # count vowels in rhyme string
        rhyme_vowel_count = sum(1 for c in rhyme if c in self.hammond_vowels)
        # if that number of vowels back in the stress string is main stress, then rhyme started
        # with main stress
        if test_word_dict['stress'][-rhyme_vowel_count] == '1':
            return True
        else:
            return False
        

class Text:
    '''Represents the text to be analyzed.'''
    def __init__(self,text,word_dict,tr=Transcriptions()):
        self.text = text
        self.lines = self._makeCleanedLines()
        self.word_dict = word_dict
        self.tr = tr

    def _makeCleanedLines(self):
        # TODO go through self.text, clean up punctuation etc., and return list of lines
        return self.text.splitlines()

    def _getLastWords(self):
        '''Split on spaces and return a list of the last word of each line.'''
        last_words = []
        for l in self.lines:
            last_words.append(l.split()[-1])
        return last_words

    def _alphafyNumericRhymeScheme(self,numeric_rhyme_scheme):
        '''Take numeric representation (e.g., '1212') of rhyme scheme and convert to alpha ('ABAB').'''
        # TODO do this in a smarter way, so that overrunning Z goes to AA or something as to allow analysis
        # of texts of arbitrary length
        return ''.join(chr(int(n)-1 + ord('A')) for n in numeric_rhyme_scheme)

    def _getRhymeSchemeFromWords(self,word_spellings):
        '''Generate a numeric rhyme scheme from a a list of words.'''
        # get rhyme of each last word
        rhymes = []
        for sp in word_spellings:
            word_data = self.word_dict.findSpelling(sp)[0] # only take the first result; TODO handle this in a more sophisticated fasion, checking all possible ones, perhaps
            rhymes.append(self.tr.getRhyme(word_data['transcription'],word_data['stress']))
        rhyme_scheme = ''
        i = 1
        seen = {}
        for r in rhymes:
            if r in seen.keys():
                rhyme_scheme += str(seen[r])
            else:
                seen[r] = i
                rhyme_scheme += str(i)
                i += 1
        return rhyme_scheme

    def getRhymeScheme(self):
        '''Return alpha rhyme scheme.'''
        last_words = self._getLastWords()
        rhyme_scheme = self._getRhymeSchemeFromWords(last_words)
        return self._alphafyNumericRhymeScheme(rhyme_scheme)

# only intended to be used interactively for testing
if __name__ == '__main__':
    wd = WordDict('../db/english_dict.db')
    poem_text = 'these are the words\nthey are for the birds\nA few just might rhyme\nif they don\'t it\'s no crime'
    t = Text(poem_text,wd)
