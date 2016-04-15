# Provides the WordDict class as a database abstraction for accessing pronunciation data
import sqlite3
import string

class WordDict:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.conn_cursor = self.connection.cursor()

    def _rowAsDict(self,row):
        d = {}
        for idx, col in enumerate(self.conn_cursor.description):
            d[col[0]] = row[idx]
        return d

    def findSpelling(self,sp):
        sp = sp.upper()
        spelling_tuple = (sp,)
        results = self.conn_cursor.execute("SELECT * FROM words WHERE spelling=?;",spelling_tuple)
        #return [r for r in results]
        return [self._rowAsDict(r) for r in results]

    def findTranscription(self,tr):
        trans_tuple = (tr,)
        results = self.conn_cursor.execute("SELECT * FROM words WHERE transcription=?;",trans_tuple)
        return [self._rowAsDict(r) for r in results]

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
            results = [rh for rh in rhyme_seg_matches if trans.isRhymeMainStressed(rhyme_segs,self._rowAsDict(rh))]

            all_results.extend(results)
        return [self._rowAsDict(r) for r in all_results]


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
        # if that number of vowels back in the stress string is main stress, then rhyme started with main stress
        if test_word_dict['stress'][-rhyme_vowel_count] == '1':
            return True
        else:
            return False
        

class Text:
    '''Represents the text to be analyzed.'''
    def __init__(self,text,word_dict,tr=Transcriptions()):
        self.text = text
        self.lines_raw = self._splitRawLines()
        self.lines_cleaned = self._makeCleanedLines()
        self.word_dict = word_dict
        self.tr = tr

    def _splitRawLines(self):
        lines = self.text.splitlines()
        # ditch whitespace-only or blank empty lines
        non_blank_lines = []
        for L in lines:
            if not (L.isspace() or L == ''):
                non_blank_lines.append(L)
        return non_blank_lines
        

    def _makeCleanedLines(self):
        lines = self.lines_raw
        cleaned_lines = []
        # ditch punctuation, numbers, and other things
        for L in lines:
            cleaned_line = ''.join(c for c in L if c in string.ascii_letters + string.whitespace)
            cleaned_lines.append(cleaned_line)
        return cleaned_lines

    def _getLastWords(self):
        '''Split on spaces and return a list of the last word of each line.'''
        last_words = []
        for l in self.lines_cleaned:
            last_words.append(l.split()[-1])
        return last_words

    def _alphafyNumericRhymeScheme(self,numeric_rhyme_scheme):
        '''Take numeric representation (e.g., '1212') of rhyme scheme and convert to alpha ('ABAB').'''
        # TODO do this in a smarter way, so that overrunning Z goes to AA or something as to allow analysis
        # of texts of arbitrary length
        alpha_rhyme_scheme = ''
        for c in numeric_rhyme_scheme:
            if c == '?':
                alpha_rhyme_scheme += '?'
            else:
                alpha_rhyme_scheme += chr(int(c)-1 + ord('A'))
        return alpha_rhyme_scheme

    def _getRhymeSchemeFromWords(self,word_spellings):
        '''Generate a numeric rhyme scheme from a a list of words.'''
        # get rhyme of each last word
        rhymes = []
        for sp in word_spellings:
            matched_spellings = self.word_dict.findSpelling(sp)
            # TODO do something to handle words that aren't in the dictionary; approximate pronunciation/syllables?
            # FIXME for now, just append Nona and move on to the next word
            if len(matched_spellings) == 0:
                rhymes.append(None)
                continue
            word_data = matched_spellings[0] # only take the first result; TODO handle this in a more sophisticated fasion, checking all possible ones, perhaps
            rhymes.append(self.tr.getRhyme(word_data['transcription'],word_data['stress']))
        rhyme_scheme = ''
        i = 1
        seen = {}
        for r in rhymes:
            if r is None:
                rhyme_scheme += '?'
                continue
            if r in seen.keys():
                rhyme_scheme += str(seen[r])
            else:
                seen[r] = i
                rhyme_scheme += str(i)
                i += 1
        return rhyme_scheme

    def _scanLine(self,line,foot_type):
        '''Scan a line for a given foot type (notated s=strong, w=weak) and return discrepancies.'''
        # TODO implement
        pass

    def _getRhymeScheme(self):
        '''Return alpha rhyme scheme.'''
        last_words = self._getLastWords()
        rhyme_scheme = self._getRhymeSchemeFromWords(last_words)
        return self._alphafyNumericRhymeScheme(rhyme_scheme)

    def getRhymeSchemeAnnotatedLines(self):
        '''Return a list of dictionaries {line_text, rhyme_word, scheme_letter} corresponding to each line'''
        annotated_lines = []
        for i in range(len(self.lines_raw)):
            line_dict = {}
            line_dict['line_text'] = self.lines_raw[i]
            line_dict['rhyme_word'] = self._getLastWords()[i]
            line_dict['scheme_letter'] = self._getRhymeScheme()[i]
            annotated_lines.append(line_dict)
        return annotated_lines

# only intended to be used interactively for testing
if __name__ == '__main__':
    wd = WordDict('../db/english_dict.db')
    poem_text = 'to walk into the room\nand sense impending doom\nabout to come and see\na feeling fresh and free'
    t = Text(poem_text,wd)
