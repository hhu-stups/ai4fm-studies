"""
Use this script to preprocess a bibtex file we organised with JabRef.
The preprocessing will remove all irrelevant fields from the bibtex entries
and clean up the groups.
Thus, the resulting bibtex file will be more readable and consistent.
"""
from importlib import resources
import io
import sys

import bibtexparser


def preprocess(bibfile_paths: list[str]):
    output = io.StringIO(newline=None)
    output.write(
        '@comment{This file was generated via `python -m dev`.}\n\n')

    for bibfile_path in bibfile_paths:
        bib = _load_bibfile(bibfile_path)

        writer = bibtexparser.bwriter.BibTexWriter()
        writer.indent = '  '  # Use 2 spaces for indentation.
        writer.contents = ['entries']
        writer.align_values = True

        bibtexparser.dump(bib, output, writer=writer)

    print(output.getvalue()[:-1])  # -1 to remove the last newline.


def _load_bibfile(bibfile_path):
    with open(bibfile_path) as bibfile:
        bib = bibtexparser.load(bibfile)

    new_entries = []
    for entry in bib.entries:
        entry = _remove_unrelated_fields(entry)
        entry = _clean_up_groups(entry)
        new_entries.append(entry)

    bib.entries = new_entries
    return bib


def _remove_unrelated_fields(bibentry: dict) -> dict:
    """
    Remove all fields from a bibtex entry that are not relevant for the
    overview. This allows to keep the entries consistent and clean.  """

    result = dict(bibentry)  # Copy to avoid modifying the original entry.
    entry_type = result['ENTRYTYPE']

    if entry_type == 'inproceedings' and 'journal' in result and 'series' not in result:
        # Fixes some entries.
       result['series'] = result['journal']

    kept_fields = _remove_unrelated_fields.fields_to_keep[entry_type]
    for field in list(result.keys()):
        if field not in kept_fields:
            del result[field]

    return result


_remove_unrelated_fields.fields_to_keep = {
    'article': [
        "author", "title", "journal", "year", "volume", "number", "pages",
    ],
    'incollection': [
        "author", "editor", "title", "booktitle", "year", "publisher", "pages"
    ],
    'inproceedings': [
        "author", "title", "booktitle", "series", "year", "pages", "publisher",
        'series', 'volume', 'number',
    ],
    'inbook': [
        "author", "title", "booktitle", "year", "publisher",
        "pages"
    ],
}
for entry_type in _remove_unrelated_fields.fields_to_keep:
    for universally_kept_field in ['doi', 'url', 'ENTRYTYPE', 'ID', 'groups']:
        _remove_unrelated_fields.fields_to_keep[entry_type].append(
            universally_kept_field)


def _clean_up_groups(bibentry):
    """
    Cleans the groups field of a bibtex entry. This field is used by JabRef
    during grouping of entries. Due to copy and pasting between different
    stages of the working process, this field can contain outdated flags.
    """

    parent_group_map = _clean_up_groups.parent_group_map

    result = dict(bibentry)  # Copy to avoid modifying the original entry.
    groups = result.get('groups', [])

    new_groups = set()
    for group in groups.split(','):
        group = group.strip()
        new_groups.update(parent_group_map.get(group, set()))

    result['groups'] = ','.join(sorted(new_groups))
    # Do not keep empty fields.
    if not result['groups']:
        del result['groups']
    return result


def _get_group_cleanup_helper_dict():
    """
    Return a dictionary that maps a group to a set of parent groups
    to replace it with.
    """
    parent_group_map = {}
    group_stack = []

    groups_csv = resources.files('dev').joinpath('groups.csv')
    with groups_csv.open('r') as groups_file:
        # Skip header line
        groups_file.readline()
        for info_line in groups_file:
            level, group_name, keep_as = info_line.strip().split(',')
            level = int(level)

            if len(keep_as) == 0 or not keep_as:
                # This group is not supposed to be kept.
                keep_as = None

            if level <= len(group_stack):
                while len(group_stack) >= level:
                    group_stack.pop()
            group_stack.append(keep_as)
            parent_group_map[group_name] = set(group_stack) - {None}
    return parent_group_map


_clean_up_groups.parent_group_map = _get_group_cleanup_helper_dict()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m dev <bibfile_1> <bibfile_2> ...")
        sys.exit(1)

    source_files = sys.argv[1:]
    preprocess(source_files)
