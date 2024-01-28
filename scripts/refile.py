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
    """ Get all files matching the regex, along with their match objects """
    all_filepaths = all_files(recursive, files_only, dirs_only)
    filematches = []
    for filepath in all_filepaths:
        filename = basename(filepath)
        for regex in regexes:
            if ignore_case:
                matches = re.finditer(regex, filename, flags=re.IGNORECASE)
            else:
                matches = re.finditer(regex, filename)
            for match in matches:
                # Append the filepath and the match object as a tuple
                filematches.append((filepath, match))
                break

    if invert_match:
        filenames_found = [f for f, _ in filematches]
        inverted_filematches = []
        for filepath in all_filepaths:
            if filepath not in filenames_found:
                inverted_filematches.append((filepath, None))
        return inverted_filematches

    return filematches


def autogroup_files(filematches, omit_single_files=True):
    """
    Heuristically group files by common naming conventions
    """
    delimiters = (' Feat. ', ' feat ', ' - ',)
    groups = {}
    for f, match in filematches:
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


def show_files(filematches):
    _dirs = []
    _files = []
    for f, _ in filematches:
        if isfile(f):
            _files.append(f)
        else:
            _dirs.append(f)
    for d in _dirs:
        print(f"🗀  {relpath(d)}")
    for f in _files:
        print(f"✔  {relpath(f)}")


def move_files_to_dir(filematches, dest_dir, dry=True, create_dirs=False):
    if create_dirs:
        try:
            os.makedirs(dest_dir)
        except FileExistsError:
            pass
    for f, match in filematches:
        target = join(dest_dir, basename(f))
        pres = f"{relpath(f)} ➜ {relpath(target)}"
        if dry:
            print(pres)
        else:
            os.replace(f, target)
            print(f"Moved file {pres}")


def move_file(orig, dest, dry=True):
    pres = f"{relpath(orig)} ➜ {relpath(dest)}"
    if dry:
        print(pres)
    else:
        os.replace(orig, dest)
        print(f"Moved file {pres}")


def delete_files(filematches, dry=True):
    for filename, match in filematches:
        if dry:
            print(f"✖ {relpath(filename)}")
        else:
            os.remove(filename)
            print(f"Deleted {relpath(filename)}")


def rename_files(filematches, pattern, dry=True):
    pattern_placeholder_count = len(re.findall(r'\$\d+', pattern))
    for filename, match in filematches:

        # Evaluate placeholders (e.g. $1, $2, ...)
        new_filename = pattern
        if match:
            
            match_group_count = len(match.groups())
            if pattern_placeholder_count > match_group_count:
                print(f"Pattern has {pattern_placeholder_count} placeholders, but only {match_group_count} groups were found in the regex")
                exit(1)

            if len(match.groups()) > 0:
                new_filename = pattern

            for i, group in enumerate(match.groups()):
                new_filename = new_filename.replace(f'${i + 1}', group)

        move_file(filename, new_filename, dry)
