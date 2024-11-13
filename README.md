# Mapping Study; title to be adjusted

## Build notes

We build the repository files with Python 3.10.
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
external researchers. The respective `search_results.bib` is available
in the dev-only repository of the article.

```sh
python preprocess_jabref_bibfile.py search_results.bib database.bib
```

To update the overview files,
edit `make_overviews.py` to your liking and run it.

```sh
python make_overviews.py
```

## Cite this repository

If you are finding use in our aggregated database of primary studies
and use it in your own research,
please consider using the following reference.

* tbd.

```bibtex
@tbd{}
```
