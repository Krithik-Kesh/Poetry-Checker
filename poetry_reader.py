

from typing import TextIO

from poetry_constants import (POETRY_FORMS_DICT, PRONUNCIATION_DICT)


def read_pronunciation(pronunciation_file: TextIO) -> PRONUNCIATION_DICT:
    """Return the pronunciation dictionary formed from reading
    pronunciation_file, an open file that is in the format of the CMU
    Pronouncing Dictionary.

    >>> small_pd = open('datasets/pronunciation_dictionary_small.txt')
    >>> word_to_phonemes = read_pronunciation(small_pd)
    >>> small_pd.close()
    >>> word_to_phonemes == {'CAMPBELL': ('K', 'AE1', 'M', 'B', 'AH0', 'L'),
    ...                      'GRIES': ('G', 'R', 'AY1', 'Z'),
    ...                      'SMITH': ('S', 'M', 'IH1', 'TH')}
    True
    """
    pronunciation_dict = {}

    for line in pronunciation_file:
        if not line.startswith(';;;'):
            parts = line.strip().split()
            word = parts[0]
            phonemes = tuple(parts[1:])
            pronunciation_dict[word] = phonemes

    return pronunciation_dict


def read_poetry_form_descriptions(poetry_forms_file: TextIO) \
        -> POETRY_FORMS_DICT:
    """Return a dictionary of poetry form name to poetry form description for
    the poetry forms in poetry_forms_file.

    >>> small_pf = open('datasets/poetry_forms_small.txt')
    >>> name_to_description = read_poetry_form_descriptions(small_pf)
    >>> small_pf.close()
    >>> name_to_description == {
    ...     'Haiku': ((5, 7, 5), ('*', '*', '*')),
    ...     'Limerick': ((8, 8, 5, 5, 8), ('A', 'A', 'B', 'B', 'A'))}
    True
    """

    poetry_dict = {}
    poetry_name = ""
    count = []
    rhyme = []

    for line in poetry_forms_file:
        new_line = line.strip()
        if new_line == "":
            if poetry_name:
                poetry_dict[poetry_name] = (tuple(count), tuple(rhyme))
                poetry_name = ""
                count = []
                rhyme = []
        elif not poetry_name:
            poetry_name = new_line
        else:
            parts = new_line.split()
            count.append(int(parts[0]))
            rhyme.append(parts[1])
    if poetry_name:
        poetry_dict[poetry_name] = (tuple(count), tuple(rhyme))

    return poetry_dict


if __name__ == '__main__':
    import doctest

