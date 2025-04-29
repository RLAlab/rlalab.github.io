import requests
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def fetch_openalex_works(author_name):
    # Step 1: Find the author ID
    response = requests.get("https://api.openalex.org/authors", params={"search": author_name})
    response.raise_for_status()
    results = response.json()["results"]
    
    if not results:
        raise ValueError("Author not found in OpenAlex.")
    
    author_id = results[0]["id"]  # Use first matched author
    display_name = results[0]["display_name"]

    # Step 2: Get publications
    works = []
    cursor = "*"
    while True:
        works_response = requests.get(
            "https://api.openalex.org/works",
            params={
                "filter": f"author.id:{author_id}",
                "per-page": 200,
                "cursor": cursor
            }
        )
        works_response.raise_for_status()
        works_page = works_response.json()
        works.extend(works_page["results"])
        cursor = works_page["meta"]["next_cursor"]
        if not cursor:
            break

    return works

def create_bibtex_entry(publication):

    authors = []
    for author in publication['authorships']:
        authors.append(author['author']['display_name'])

    try: 
        journal = publication['primary_location']['source']["display_name"]
    except:
        journal = ''

    try:
        if publication['doi']:
            url = publication['doi']
        else:
            url = publication['primary_location']['landing_page_url']
    except:
        url = publication['primary_location']['landing_page_url']

    bib_entry = {
        "ENTRYTYPE": publication.get('type', 'article'),
        "ID": publication.get('id', 'unknown_id'),
        "title": publication.get('title', ''),
        "author": ' and '.join(authors),
        "journal": journal,
        "year": str(publication.get('publication_year', '')),
        "url": url
    }
    return bib_entry

# Fetch and filter
author_name = "Rodrigo Ledesma-Amaro"
works = fetch_openalex_works(author_name)

bib_entries = []
for work in works:
    try: 
        work['primary_location']['landing_page_url']
        bib_entries.append(create_bibtex_entry(work))
    except:
        continue

# Write to .bib file
bib_database = BibDatabase()
bib_database.entries = bib_entries
writer = BibTexWriter()

with open("publications.bib", "w") as f:
    f.write(writer.write(bib_database))