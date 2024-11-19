# Application of AI to formal methods

This repository contains a data set of 457 scientific publications
which apply artificial intelligence onto the area of formal methods.
The data were aggregated within scope of a
systematic mapping study which can be found
[here](#cite-this-repository).

For the five year span of 2019-2023 consisting of 189 publications,
we conducted a mapping study and sorted the entries according to their
utilized AI technique and their respective application domain within
the formal methods research area.

We provide the following files:

* [`database.bib`](database.bib):
  The full list of found publications, in Bibtex format.
  Processed entries have a `groups` field attached. See also
  [`groups.csv`](groups.csv).
* [`overview/ai-techniques_2019-2023.md`](overview/ai-techniques_2019-2023.md):
  List of the processed publications from 2019-2023, grouped by their utilized
  AI technique.
* [`overview/fm-techniques_2019-2023.md`](overview/fm-techniques_2019-2023.md):
  List of the processed publications from 2019-2023, grouped by their utilized
  FM technique.
* [`overview/all_by_year.md`](overview/all_by_year.md):
  List of all entries divided by their respective publication years.

More information on how we assembled the data can be found in
our systematic mapping study.

## Cite this repository

If you are finding use in our aggregated database of primary studies
within your own research,
please consider using the following reference.

* tbd.

```bibtex
@tbd{}
```

## Build notes

We build the repository files with Python 3.10+.
You can optionally choose to prepare a virtual environment.
Dependencies are stored in
[`requirements.txt`](requirements.txt) as usual.

```sh
# Setup virtual environment (optional but recommended)
python3.10 -m venv env
. env/bin/activate
# Install dependencies
pip install -r requirements.txt
```

If you want to update the underlying search results, run the preprocessing
first. The preprocessed version is checked in for easier use by
external researchers. The respective
`search_results.bib` and `not_in_time_frame.bib` files
are available
in the dev-only repository of the article.

```sh
python -m dev search_results.bib not_in_time_frame.bib > database.bib
```

To update the overview files,
edit `make_overviews.py` to your liking and run it.

```sh
python make_overviews.py
```
