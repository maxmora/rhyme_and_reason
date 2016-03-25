#!/usr/env python3
import string
import Transcriptions

# FIXME should be done more smartly
def strip_trailing_paren_num_from_string(s):
    '''Remove '([0-9])' from the end of a string, used to remove
       homograph numbers (which CMU dict list parenthetically) from
       spelling strings, so that such words are actually homographic.
       Current implementation not very robust.'''
    if s[-1:] == ')' and s[-3:-2] == '(':
        s = s[:-3]
    return s

def to_numeric_stress_pattern(phone_string):
    '''Make a string of just the numerals in the non-split string of phones.
       This represents the stress pattern of the word.'''
    return ''.join(c for c in phone_string if c in string.digits)

def to_stressless_phone_string(phone_string):
    '''Remove numerals from a phone string, keeping just the segmental
       information.'''
    return ''.join(c for c in phone_string if c not in string.digits)

def parse_line_hammond(L,arpa_to_hammond):
    '''Parses a valid line of CMU dictionary into a Python dict with the word's
       'spelling', 'transcription', and numeric 'stress' pattern.'''
    word_props = {}
    word, phones = L.split('  ')
    word_props['spelling'] = strip_trailing_paren_num_from_string(word)
    # hammondize phone string
    destressed_phone_string = to_stressless_phone_string(phones)
    word_props['transcription'] = ''.join(arpa_to_hammond[p] for p in destressed_phone_string.split())
    word_props['stress'] = to_numeric_stress_pattern(phones)
    return word_props

def parse_to_list_hammond(data_lines,arpa_to_hammond):
    parsed_data_list= []
    for L in data_lines:
        # ignore commented lines starting with ';;;'
        if L[:3] == ';;;':
            continue
        parsed_data_list.append(parse_line_hammond(L,arpa_to_hammond))
    return parsed_data_list

def generate_word_list_from_file(f):
    indict = open(f)
    data = indict.read().splitlines()

    t = Transcriptions.Transcriptions()
    arpa_to_hammond = t.arpabet_to_hammond_dict

    parsed = parse_to_list_hammond(data,arpa_to_hammond)
    return parsed
    


# DEPRECATED FUNCTION GRAVEYARD

# need to be re-written to not use dict's if these are to be used
def parse_line_arpabet(L,data_dict):
    word_props = {}
    word, phones = L.split('  ')
    word_props['phones'] = phones.split()
    word_props['stress'] = to_numeric_stress_pattern(phones)
    data_dict[word] = word_props
def parse_to_dict_arpabet(data):
    parsed_data_dict = {}
    for L in data:
        # ignore commented lines starting with ';;;'
        if L[:3] == ';;;':
            continue
        parse_line_arpabet(L,parsed_data_dict)
    return parsed_data_dict
