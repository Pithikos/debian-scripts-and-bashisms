import os
import re
import sys
from copy import copy
from glob import glob
from os.path import join, basename, relpath, isfile, dirname


def all_files(recursive=False, files_only=False, dirs_only=False):
    """ Get all offspring files under current directory """
    all_entities = glob(join(os.getcwd(), '*'), recursive=recursive)
    if not files_only and not dirs_only:
        return all_entities
    if files_only:
        return [e for e in all_entities if isfile(e)]
    if dirs_only:
        return [e for e in all_entities if not isfile(e)]


def get_matching_files(regexes, recursive, ignore_case, files_only, dirs_only, invert_match):
    """ Get all files matching the regex """
    all_filepaths = all_files(recursive, files_only, dirs_only)
    matched = []
    for filepath in all_filepaths:
        filename = basename(filepath)
        for regex in regexes:
            if ignore_case:
                matches = re.findall(regex, filename, flags=re.IGNORECASE)
            else:
                matches = re.findall(regex, filename)
            if matches:
                matched.append(filepath)
                break
    if invert_match:
        matched = set(all_filepaths) - set(matched)
    return matched


def autogroup_files(files, omit_single_files=True):
    """
    Heuristically group files by common naming conventions
    """
    delimiters = (' Feat. ', ' feat ', ' - ',)
    groups = {}
    for f in files:
        filename = basename(f)
        for deli in delimiters:
            items = filename.split(deli)
            if len(items) < 2:
                continue
            left = items[0]
            try:
                groups[left].append(f)
            except KeyError:
                groups[left] = [f]
            break

    # Remove groups that only hold single files_only
    if omit_single_files:
        for k in list(groups.keys()):
            if len(groups[k]) <= 1:
                del groups[k]

    if not groups:
        return groups

    # Titleze all if most are already titleized
    is_titletized = ([k.istitle() for k in groups.keys()].count(True) / len(groups)) > 0.6
    if is_titletized:
        new_groups = {}
        for k in groups.keys():
            new_groups[k.title()] = groups[k]
        groups = new_groups

    return groups


def show_files(files):
    _dirs = []
    _files = []
    for f in files:
        if isfile(f):
            _files.append(f)
        else:
            _dirs.append(f)
    for d in _dirs:
        print(f"🗀  {relpath(d)}")
    for f in _files:
        print(f"✔  {relpath(f)}")


def move_file(orig, dest, dry=True):
    pres = f"{relpath(orig)} ➜ {relpath(dest)}"
    if dry:
        print(pres)
    else:
        os.replace(orig, dest)
        print(f"Moved file {pres}")


def move_files_to_dir(files, dest_dir, dry=True, create_dirs=False):
    if create_dirs:
        try:
            os.makedirs(dest_dir)
        except FileExistsError:
            pass
    for f in files:
        target = join(dest_dir, basename(f))
        pres = f"{relpath(f)} ➜ {relpath(target)}"
        if dry:
            print(pres)
        else:
            os.replace(f, target)
            print(f"Moved file {pres}")


def delete_files(files, dry=True):
    for f in files:
        if dry:
            print(f"✖ {relpath(f)}")
        else:
            os.remove(f)
            print(f"Deleted {relpath(f)}")


def eval_filename_pattern(filepath, pattern):
    if ':' not in pattern:
        raise Exception("Must user two regular expressions separated with colon e.g. '(.*).jpg.bak:$1.jpg'")

    re_from, re_to = pattern.split(":")
    filename = basename(filepath)

    # Find matches in original filename
    matches = re.match(re_from, filename).groups()

    # Rebuild filename
    placeholders = re.findall('\$[0-9]*', re_to)
    if len(placeholders) < len(matches):
        raise Exception(f"Expected {len(matches)} placeholders, got {len(placeholders)}")
    new_filename = re_to.lstrip(" ")
    for i, matched_string in enumerate(matches, 1):
        new_filename = new_filename.replace(f"${i}", matched_string)

    return join(dirname(filepath), new_filename.strip())


def rename_files(files, pattern, dry=True):
    for f in files:
        target = eval_filename_pattern(f, pattern)
        move_file(f, target, dry)
