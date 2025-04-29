import requests
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import re
import html
import unicodedata

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

def normalize_title(title):
    """remove HTML tags and normalize unicode."""
    title = html.unescape(title)                         # convert HTML entities like &lt; to <
    title = re.sub(r'<[^>]+>', '', title)                # remove HTML tags like <i>
    title = unicodedata.normalize('NFKD', title)         # normalize accented characters
    title = re.sub(r'\s+', ' ', title).strip()           # normalize whitespace, lowercase
    return title

def create_bibtex_entry(publication):
    authors = [a['author']['display_name'] for a in publication['authorships']]
    try: 
        journal = publication['primary_location']['source']["display_name"]
    except:
        journal = ''
    try:
        url = publication['doi'] if publication['doi'] else publication['primary_location']['landing_page_url']
    except:
        url = publication['primary_location']['landing_page_url']

    title = normalize_title(publication['title'])
    bib_entry = {
        "ENTRYTYPE": publication.get('type', 'article'),
        "ID": publication.get('id', 'unknown_id'),
        "title": title,
        "author": ' and '.join(authors),
        "journal": journal,
        "year": str(publication.get('publication_year', '')),
        "url": url
    }
    return bib_entry

# Fetch and filter
author_name = "Rodrigo Ledesma-Amaro"
works = fetch_openalex_works(author_name)

# Deduplication logic
seen = {}
bib_entries = []

for work in works:
    try:
        title_norm = normalize_title(work['title'])
        year = str(work.get('publication_year', ''))
        key = ','.join([a['author']['display_name'] for a in work['authorships']])

        if key in seen:
            # Prefer peer-reviewed over preprint if duplicate found
            existing = seen[key]
            if existing['ENTRYTYPE'] == 'preprint' and work.get('type') != 'preprint':
                seen[key] = create_bibtex_entry(work)
        else:
            seen[key] = create_bibtex_entry(work)
    except Exception as e:
        continue

bib_entries = list(seen.values())

# Write to .bib
bib_database = BibDatabase()
bib_database.entries = bib_entries
writer = BibTexWriter()

with open("publications.bib", "w") as f:
    f.write(writer.write(bib_database))