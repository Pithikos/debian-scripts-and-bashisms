import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(__file__)))

from refile import *


def test_autogroup_files():
    assert autogroup_files(['a', 'ab'], omit_single_files=False) == {}
    assert autogroup_files(['P E N S E E S _ Murky.opus'], omit_single_files=False) == {}

    f = 'a b Feat. c - whatever.mp3'
    assert autogroup_files([f], omit_single_files=False) == {'a b': [f]}

    f = "Abhi The Nomad - Sex n' Drugs (feat. Harrison Sands & Copper King) [Official Lyric Video]"
    assert autogroup_files([f], omit_single_files=False) == {'Abhi The Nomad': [f]}


def test_autogroup_files_titleize():
    files = [
        'a - song.mp3',
        'B - song.mp3',
        'C - song.mp3',
    ]
    assert autogroup_files(files, omit_single_files=False) == {
        'A': ['a - song.mp3'],
        'B': ['B - song.mp3'],
        'C': ['C - song.mp3'],
    }
    assert autogroup_files(files, omit_single_files=True) == {}


def test_move_files():
    # TODO: ..
    pass


def test_eval_filename_pattern():
    # Asterisk
    assert eval_filename_pattern("my_file.txt", "_: test-{*}") == "test-my_file.txt"

    # File parts
    assert eval_filename_pattern("my_file.txt", "_: {2}-{1}.{ext}") == "file-my.txt"
    assert eval_filename_pattern(
        "1970_September_Statement.pdf", "_: bank-statement-{1}-{2}.{ext}") == \
        "bank-statement-1970-September.pdf"

    # Paths
    assert eval_filename_pattern("/my_dir/my_file.txt", "_: test-{*}") == "/my_dir/test-my_file.txt"
