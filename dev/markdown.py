from bibtexparser.latexenc import latex_to_unicode

def entry_to_markdown(bibentry):
    """
    Converts a bibtex entry to markdown format.
    """
    entry_type = bibentry['ENTRYTYPE']

    if entry_type == 'article':
        return _article_to_markdown(bibentry)
    elif entry_type == 'incollection':
        return _incollection_to_markdown(bibentry)
    elif entry_type == 'inproceedings':
        return _inproceedings_to_markdown(bibentry)
    elif entry_type == 'inbook':
        return _inbook_to_markdown(bibentry)
    else:
        raise ValueError(f'Entrytype {entry_type} not supported.')


def bibtex_link_text(key):
    """
    Returns the markdown text for a bibtex link.
    """
    line = bibtex_link_text.key_to_lino[key]
    return f'[[bibtex](../database.bib#L{line})]'
bibtex_link_text.key_to_lino = {}
with open('database.bib') as db:
    lines = db.readlines()
    for i, line in enumerate(lines):
        if line.startswith('@'):
            key = line.strip().split('{')[1][:-1]  # '@article{key,' -> 'key'
            bibtex_link_text.key_to_lino[key] = i+1


def doi_url_bib_info(bibentry):
    """
    Returns the markdown text for a DOI or URL.
    """
    doi = bibentry.get('doi', None)
    url = bibentry.get('url', None)
    out = ' '
    if doi:
        if not doi.startswith('http'):
            doi = f'http://dx.doi.org/{doi}'
        out += f'[[doi]({doi})]'
    elif url:
        out += f'[[url]({url})]'
    out += bibtex_link_text(bibentry['ID'])

    return out


def _article_to_markdown(bibentry):
    """
    Converts an article bibtex entry to markdown format.
    """
    author = bibentry.get('author', 'Unknown author')
    title = bibentry.get('title', 'Unknown title')
    journal = bibentry.get('journal', 'Unknown journal')
    year = bibentry.get('year', 'Unknown year')
    volume = bibentry.get('volume', None)
    number = bibentry.get('number', None)
    pages = bibentry.get('pages', None)

    author_year = latex_to_unicode(f'{author} ({year}).')
    title = latex_to_unicode(f'{title}.')

    venue = f'In _{latex_to_unicode(journal)}_'
    if volume:
        venue += f' {volume}'
        if number:
            venue += f'({number})'
    if pages:
        venue += f', p. {latex_to_unicode(pages)}'
    venue += '.'

    out = f'{author_year} {title} {venue}'
    out += doi_url_bib_info(bibentry)


    return out


def _incollection_to_markdown(bibentry):
    """
    Converts an incollection bibtex entry to markdown format.
    """

    author = bibentry.get('author', 'Unknown author')
    title = bibentry.get('title', 'Unknown title')
    booktitle = bibentry.get('booktitle', 'Unknown booktitle')
    year = bibentry.get('year', 'Unknown year')
    publisher = bibentry.get('publisher', None)
    pages = bibentry.get('pages', None)

    author_year = latex_to_unicode(f'{author} ({year}).')
    title = latex_to_unicode(f'{title}.')

    venue = f'In _{latex_to_unicode(booktitle)}_.'
    if publisher:
        venue += f' {latex_to_unicode(publisher)}'
    if pages:
        venue += f' p. {latex_to_unicode(pages)}'
    venue += '.'

    out = f'{author_year} {title} {venue}'
    out += doi_url_bib_info(bibentry)

    return out


def _inproceedings_to_markdown(bibentry):
    """
    Converts an inproceedings bibtex entry to markdown format.
    """
    author = bibentry.get('author', 'Unknown author')
    title = bibentry.get('title', 'Unknown title')
    booktitle = bibentry.get('booktitle', 'Unknown proceedings')
    series = bibentry.get('series', None)
    year = bibentry.get('year', 'Unknown year')
    pages = bibentry.get('pages', None)
    publisher = bibentry.get('publisher', None)
    series = bibentry.get('series', None)
    volume = bibentry.get('volume', None)
    number = bibentry.get('number', None)

    author_year = latex_to_unicode(f'{author} ({year}).')
    title = latex_to_unicode(f'{title}.')

    venue = f'In _{latex_to_unicode(booktitle)}_'
    if series:
        venue += f', {series}'
    if volume:
        venue += f' {volume}'
        if number:
            venue += f'({number})'
    if pages:
        venue += f', p. {latex_to_unicode(pages)}'
    venue += '.'
    if publisher:
        venue += f' {latex_to_unicode(publisher)}.'

    out = f'{author_year} {title} {venue}'
    out += doi_url_bib_info(bibentry)

    return out


def _inbook_to_markdown(bibentry):
    """
    Converts an inbook bibtex entry to markdown format.
    """
    return _incollection_to_markdown(bibentry)
