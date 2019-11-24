import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(__file__)))

from refile import autogroup_files


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
