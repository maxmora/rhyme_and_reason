# Rhyme and Reason

Rhyme and Reason is a searchable phonological/rhyming dictionary with a Bottle-based REST API. The respository also includes scripts to convert data from the CMU Pronouncing Dictionary to a format based on that used in the dictionary formerly at http://lexicon.arizona.edu/~hammond/newdic.html.

Other fuctionality is being implemented for analysis of poetic rhyme schemes and metrics.

# API Overview

## Spelling

Sending a GET request to `URL/spelling/WORD` will return a JSON representation of the words, transcriptions, and stress patterns for all entries with the spelling `WORD`.


## Transcription

Sending a GET request to `URL/transcription/TRANSCRIPTION` will return a JSON representation of the words, transcriptions, and stress patterns for all entries with the phonological form `TRANSCRIPTION`.


## Rhymes

Sending a GET request to `URL/rhyme/WORD` will return a JSON representation of the words, transcriptions, and stress patterns for all entries that rhyme with `WORD`. This is computed on the fly by selecting all words with matching segments from the primary-stressed vowel to the end of the word.
