import pytest
from poetry_functions import get_last_syllable

def test_get_last_syllable_empty():
    """Test get_last_syllable on an empty tuple."""

    actual = poetry_functions.get_last_syllable(())
    expected = ()
    assert actual == expected, 'Expected an empty tuple'


def test_single_vowel():
    """Test with single vowel phoneme."""
    assert get_last_syllable(('IH0',)) == ('IH0',)

def test_no_vowels():
    """Test with only consonants."""
    assert get_last_syllable(('B', 'S', 'T')) == ()

def test_vowel_at_end():
    """Test with a vowel at the last phoneme."""
    assert get_last_syllable(('AE1', 'IH0')) == ('IH0',)

def test_empty():
    """Test with empty."""
    assert get_last_syllable(()) == ()

if __name__ == '__main__':
    pytest.main(['test_get_last_syllable.py'])
