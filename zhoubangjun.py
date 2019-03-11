import scholarly


def make_row(source, citation_bib, author, is_first_author):
    data = []
    data.append(source.bib['title'])

    data.append(citation_bib.get('title', ''))
    data.append(citation_bib.get('journal', ''))
    data.append(citation_bib.get('publisher', ''))
    data.append(citation_bib.get('url', ''))
    data.append(citation_bib.get('eprint', ''))

    author_name = author if isinstance(author, str) else author.name
    data.append(author_name)
    data.append(str(is_first_author))
    affiliation = author.affiliation if hasattr(author, 'affiliation') else ''
    data.append(affiliation)
    email = author.email if hasattr(author, 'email') else ''
    data.append(email)

    return '\t'.join(data)

authors = {}

def get_author(name):
    if name not in authors:
        try: 
            search_query = scholarly.search_author(name)
            author = next(search_query).fill()
            authors[name] = author
        except:
            print('Cannot find author: ' + name)
            authors[name] = name

    return authors[name]

publications = {}

def get_publication(bib):
    title = bib['title']
    if title not in publications:
        try:
            search_query = scholarly.search_pubs_query(title)
            publication = next(search_query).fill()
            publications[title] = publication.bib
        except:
            print('Cannot find publication: ' + title)
            publications[title] = bib

    return publications[title]



search_query = scholarly.search_author('Bangjun Zhou')
bangjun = next(search_query).fill()

columns = ['Source', 'Title', 'Journal', 'Publisher', 'Url', 'PDF', 'Author', 'Affiliation', 'Email']
s = '\t'.join(columns)

count = 0
for pub in bangjun.publications:
    publication = pub.fill()
    for citedby in pub.get_citedby():
        bib = citedby.bib
        citation_bib = get_publication(bib)
        author_names = citation_bib['author'].split(' and ')
        count = count + 1
        print('Processing citaiton ' + str(count) + ': ' + str(author_names))
        for idx, name in enumerate(author_names):
            author = get_author(name)
            is_first_author = idx == 0
            row = make_row(publication, citation_bib, author, is_first_author)
            s = s + '\n' + row

f = open("result.tsv", "w")
f.write(s)
    