# This file contains just a dictionary for converting stress number-less Arpabet transcriptions
# to the transcription system found in the formerly active http://lexicon.arizona.edu/~hammond/newdic.html

# Relevant text explanation of the system from the page:

#Vowels
#Symbol  Example Symbol  Example
#@   cat     E   bet
#I   bit     U   good
#O   toy     i   beet
#e   bait    u   mood
#o   mode    a   knot
#Y   might   W   bout
#c   ought   R   bird
#X   butter  x   coda
#L   bottle
#
#Consonants
#
#We only list the special consonant symbols here.
#
#Symbol  Example Symbol  Example
#T   bath    D   bathe
#S   bash    Z   measure
#C   chin    J   John
#G   sing

class Transcriptions:

    arpabet_to_hammond_dict = {
        'AA' : 'a',
        'AE' : '@',
        'AH' : 'x',
        'AO' : 'c',
        'AW' : 'W',
        'AY' : 'Y',
        'EH' : 'E',
        # TODO Hammond dictionary distinguishes X "butter" from R "bird" (unstressed vs. stress schwar)
        # This will probably depend on stress of Arpabet "ER", but this has to be investigated.
        'ER' : 'R',
        'EY' : 'e',
        'IH' : 'I',
        'IY' : 'i',
        'OW' : 'o',
        'OY' : 'O',
        'UH' : 'U',
        'UW' : 'u',


        'B'  : 'b',
        'CH' : 'C',
        'D'  : 'd',
        'DH' : 'D',
        'F'  : 'f',
        'G'  : 'g',
        'HH' : 'h',
        'JH' : 'J',
        'K'  : 'k',
        # TODO Hammond dictionary distinguishes 'L' as syllabic /l/; CMU dictionary transcribes this as schwa + /l/
        # If proper conversion of this is desired, this should be handled, otherwise, it should be noted how this works
        # in user interface
        'L'  : 'l',
        'M'  : 'm',
        'N'  : 'n',
        'NG' : 'G',
        'P'  : 'p',
        'R'  : 'r',
        'S'  : 's',
        'SH' : 'S',
        'T'  : 't',
        'TH' : 'T',
        'V'  : 'v',
        'W'  : 'w',
        'Y'  : 'j',
        'Z'  : 'z',
        'ZH' : 'Z'
        
    }     
      
    arpa_to_hammond_stress_notation_dict = {
        '0' : '_',
        '2' : '`',
        '1' : "'"
    }

    arpabet_vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']

    hammond_vowels = ['a', '@', 'x', 'c', 'W', 'Y', 'E', 'R', 'e', 'I', 'i', 'o', 'O', 'U', 'u']

