from poetry_constants import (POEM_LINE, POEM, PHONEMES, PRONUNCIATION_DICT,
                              POETRY_FORM_DESCRIPTION)

def transform_string(s: str) -> str:
    """Return a new string based on s in which all letters have been
    converted to uppercase and punctuation characters have been stripped
    from both ends. Inner punctuation is left untouched.

    >>> transform_string('Birthday!!!')
    'BIRTHDAY'
    >>> transform_string('"Quoted?"')
    'QUOTED'
    >>> transform_string('To be? Or not to be?')
    'TO BE? OR NOT TO BE'
    """

    punctuation = """!"'`@$%^&_-+={}|\\/,;:.-?)([]<>*#\n\t\r"""
    result = s.upper().strip(punctuation)
    return result


def is_vowel_phoneme(phoneme: str) -> bool:
    """Return True if and only if phoneme is a vowel phoneme. That is, whether
    phoneme ends in a 0, 1, or 2.

    Preconditions:
     - len(phoneme) > 0 and phoneme.isupper()

    >>> is_vowel_phoneme('AE0')
    True
    >>> is_vowel_phoneme('DH')
    False
    >>> is_vowel_phoneme('IH2')
    True
    """

    return phoneme[-1] in '012'


def get_syllable_count(poem_line: POEM_LINE,
                       word_to_phonemes: PRONUNCIATION_DICT) -> int:
    """Return the number of syllables in poem_line by using the pronunciation
    dictionary word_to_phonemes.

    Preconditions:
     - len(poem_line) > 0

    >>> line = 'Then! the #poem ends.'
    >>> word_to_phonemes = {'THEN': ('DH', 'EH1', 'N'),
    ...                     'ENDS': ('EH1', 'N', 'D', 'Z'),
    ...                     'THE': ('DH', 'AH0'),
    ...                     'POEM': ('P', 'OW1', 'AH0', 'M')}
    >>> get_syllable_count(line, word_to_phonemes)
    5
    """
    poem_lines = transform_string(poem_line)
    count = 0
    for i in poem_lines:
        if i in word_to_phonemes:
            for j in word_to_phonemes:
                if is_vowel_phoneme(j):
                    count += 1
    return count


def check_syllable_counts(poem_lines: POEM,
                          description: POETRY_FORM_DESCRIPTION,
                          word_to_phonemes: PRONUNCIATION_DICT) \
        -> list[POEM_LINE]:
    """Return a list of lines from poem_lines that do NOT have the right
    number of syllables as specified by the poetry form description, according
    to the pronunciation dictionary word_to_phonemes.  If all lines have the
    right number of syllables, return the empty list.

    Preconditions:
     - len(poem_lines) == len(description[0])

    >>> poem_lines = ['The first line leads off,',
    ...               'With a gap before the next.', 'Then the poem ends.']
    >>> description = ((5, 5, 4), ('*', '*', '*'))
    >>> word_to_phonemes = {'NEXT': ('N', 'EH1', 'K', 'S', 'T'),
    ...                     'GAP': ('G', 'AE1', 'P'),
    ...                     'BEFORE': ('B', 'IH0', 'F', 'AO1', 'R'),
    ...                     'LEADS': ('L', 'IY1', 'D', 'Z'),
    ...                     'WITH': ('W', 'IH1', 'DH'),
    ...                     'LINE': ('L', 'AY1', 'N'),
    ...                     'THEN': ('DH', 'EH1', 'N'),
    ...                     'THE': ('DH', 'AH0'),
    ...                     'A': ('AH0',),
    ...                     'FIRST': ('F', 'ER1', 'S', 'T'),
    ...                     'ENDS': ('EH1', 'N', 'D', 'Z'),
    ...                     'POEM': ('P', 'OW1', 'AH0', 'M'), 'OFF': ('AO1', 'F')}
    >>> check_syllable_counts(poem_lines, description, word_to_phonemes)
    ['With a gap before the next.', 'Then the poem ends.']
    >>> poem_lines = ['The first line leads off,']
    >>> description = ((0,), ('*',))
    >>> check_syllable_counts(poem_lines, description, word_to_phonemes)
    []
    """
    syllable_counts = description[0]
    invalid_lines = []
    for i in range(len(poem_lines)):
        line = poem_lines[i]
        req_syllables = syllable_counts[i]

        if req_syllables != 0:
            actual_syllables = get_syllable_count(line, word_to_phonemes)
            if actual_syllables != req_syllables:
                invalid_lines.append(line)
    return invalid_lines


def get_last_syllable(word_phonemes: PHONEMES) -> PHONEMES:
    """Return the last syllable from word_phonemes.

    The last syllable in word_phonemes is formed from the last vowel phoneme
    and any subsequent consonant phoneme(s) in word_phonemes, in the same
    order as they appear in word_phonemes.

    >>> get_last_syllable(('AE1', 'B', 'S', 'IH0', 'N', 'TH'))
    ('IH0', 'N', 'TH')
    >>> get_last_syllable(('IH0', 'N'))
    ('IH0', 'N')
    >>> get_last_syllable(('B', 'S'))
    ()
    """
    for i in range(len(word_phonemes) - 1, -1, -1):
        if is_vowel_phoneme(word_phonemes[i]):
            return word_phonemes[i:]
    return ()


def words_rhyme(word1: str, word2: str, word_to_phonemes: PRONUNCIATION_DICT) \
        -> bool:
    """Return True if and only if word1 and word2 rhyme according to
    word_to_phonemes.

    Recall that two words rhyme if and only if they have the same last
    syllable.  The two words may also contain trailing punctuation.

    >>> word_to_phonemes = {'THINE': ('DH', 'AY1', 'N'),
                            'DEVINE': ('D', 'AH0', 'V', 'AY1', 'N'),
                            'HEARD': ('HH', 'ER1', 'D')}
    >>> words_rhyme('thine', 'devine', word_to_phonemes)
    True
    >>> words_rhyme('thine', 'heard.', word_to_phonemes)
    False
    """
    word1 = transform_string(word1)
    word2 = transform_string(word2)

    if (word1 not in word_to_phonemes) or (word2 not in word_to_phonemes):
        return False

    phoneme1 = word_to_phonemes[word1]
    phoneme2 = word_to_phonemes[word2]
    last_syll1 = get_last_syllable(phoneme1)
    last_syll2 = get_last_syllable(phoneme2)

    return last_syll1 == last_syll2


def all_lines_rhyme(poem_lines: POEM, lines_to_check: list[int],
                    word_to_phonemes: PRONUNCIATION_DICT) -> bool:
    """Return True if and only if the lines from poem_lines with index in
    lines_to_check all rhyme, according to word_to_phonemes.

    Preconditions:
     - lines_to_check != []

    >>> poem_lines = ['The mouse', 'in my house', 'electric.']
    >>> lines_to_check = [0, 1]
    >>> word_to_phonemes = {'THE': ('DH', 'AH0'),
    ...                     'MOUSE': ('M', 'AW1', 'S'),
    ...                     'IN': ('IH0', 'N'),
    ...                     'MY': ('M', 'AY1'),
    ...                     'HOUSE': ('HH', 'AW1', 'S'),
    ...                     'ELECTRIC': ('IH0', 'L', 'EH1', 'K',
    ...                                  'T', 'R', 'IH0', 'K')}
    >>> all_lines_rhyme(poem_lines, lines_to_check, word_to_phonemes)
    True
    >>> lines_to_check = [0, 1, 2]
    >>> all_lines_rhyme(poem_lines, lines_to_check, word_to_phonemes)
    False
    >>> lines_to_check = [2]
    >>> all_lines_rhyme(poem_lines, lines_to_check, word_to_phonemes)
    True
    """
    last = []

    for i in lines_to_check:
        ending_word = transform_string(poem_lines[i].split()[-1])
        if ending_word not in word_to_phonemes:
            return False
        phonemes = word_to_phonemes[ending_word]
        last.append(get_last_syllable(phonemes))
    for j in last:
        if j != last[0]:
            return False
    return True


def get_rhyme_label_to_lines(rhyme_scheme: tuple[str, ...]
                             ) -> dict[str, list[int]]:
    """Return a dictionary where each key is an item in rhyme_scheme and
    its corresponding value is a list of the indexes in rhyme_scheme where
    the item appears.

    >>> result = get_rhyme_label_to_lines(('A', 'A', 'B', 'B', 'A'))
    >>> expected = {'A': [0, 1, 4], 'B': [2, 3]}
    >>> expected == result
    True
    >>> result = get_rhyme_label_to_lines(('*', '*', '*', '*', '*'))
    >>> expected = {'*': [0, 1, 2, 3, 4]}
    >>> expected == result
    True
    """
    labels = {}
    for i in range(len(rhyme_scheme)):
        label = rhyme_scheme[i]
        if label not in labels:
            labels[label] = []
        labels[label].append(i)

    return labels


def check_rhyme_scheme(poem_lines: POEM,
                       description: POETRY_FORM_DESCRIPTION,
                       word_to_phonemes: PRONUNCIATION_DICT) \
        -> list[list[POEM_LINE]]:
    """Return a list of lists of lines from poem_lines that do NOT rhyme with
    each other as specified by the poetry form description, according to the
    pronunciation dictionary word_to_phonemes. If all lines rhyme as they
    should, return the empty list.  The lines in each inner list should be
    in the same order as they appear in poem_lines.

    Preconditions:
     - len(poem_lines) == len(description[1])

    >>> poem_lines = ['The first line leads off,',
    ...               'With a gap before the next.', 'Then the poem ends.']
    >>> description = ((5, 7, 5), ('A', 'B', 'A'))
    >>> word_to_phonemes = {'NEXT': ('N', 'EH1', 'K', 'S', 'T'),
    ...                     'GAP': ('G', 'AE1', 'P'),
    ...                     'BEFORE': ('B', 'IH0', 'F', 'AO1', 'R'),
    ...                     'LEADS': ('L', 'IY1', 'D', 'Z'),
    ...                     'WITH': ('W', 'IH1', 'DH'),
    ...                     'LINE': ('L', 'AY1', 'N'),
    ...                     'THEN': ('DH', 'EH1', 'N'),
    ...                     'THE': ('DH', 'AH0'),
    ...                     'A': ('AH0',),
    ...                     'FIRST': ('F', 'ER1', 'S', 'T'),
    ...                     'ENDS': ('EH1', 'N', 'D', 'Z'),
    ...                     'POEM': ('P', 'OW1', 'AH0', 'M'),
    ...                     'OFF': ('AO1', 'F')}
    >>> bad_lines = check_rhyme_scheme(poem_lines, description,
    ...                                word_to_phonemes)
    >>> bad_lines.sort()
    >>> bad_lines
    [['The first line leads off,', 'Then the poem ends.']]
    """
    rhyme_scheme = description[1]
    labels = get_rhyme_label_to_lines(rhyme_scheme)
    bad_lines = []

    for label, j in labels.items():
        if label != '*':
            line = [poem_lines[i] for i in j]
            if not all_lines_rhyme(poem_lines, j, word_to_phonemes):
                bad_lines.append(line)

            if not all_lines_rhyme(poem_lines, j, word_to_phonemes):
                bad_lines.append(line)

    return bad_lines


if __name__ == '__main__':
    import doctest
