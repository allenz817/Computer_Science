import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'folder_with_twttr'))
import pytest
import twttr

def test_word():
    input = "twitter"
    assert twttr.shorten(input) == "twttr"

def test_sentence():
    input = "What's your name?"
    assert twttr.shorten(input) == "Wht's yr nm?"

def test_number():
    input = "CS50"
    assert twttr.shorten(input) == "CS50"

