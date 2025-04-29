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
    print(f"Found author: {display_name} ({author_id})")

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

def create_bibtex_entry(work):
    bib_entry = {
        "ENTRYTYPE": "article",
        "ID": work["id"].split("/")[-1],
        "title": work.get("title", ""),
        "author": " and ".join([a["author"]["display_name"] for a in work.get("authorships", [])]),
        "journal": work.get("host_venue", {}).get("display_name", ""),
        "volume": work.get("biblio", {}).get("volume", ""),
        "number": work.get("biblio", {}).get("issue", ""),
        "pages": work.get("biblio", {}).get("first_page", ""),
        "year": str(work.get("publication_year", "")),
        "publisher": work.get("host_venue", {}).get("publisher", ""),
        "url": work.get("id", "")
    }
    return bib_entry

# Fetch and filter
author_name = "Rodrigo Ledesma-Amaro"
works = fetch_openalex_works(author_name)

bib_entries = []
for work in works:
    if work.get("publication_year") and work.get("host_venue", {}).get("display_name"):
        bib_entries.append(create_bibtex_entry(work))

# Write to .bib file
bib_database = BibDatabase()
bib_database.entries = bib_entries
writer = BibTexWriter()

with open("publications.bib", "w") as f:
    f.write(writer.write(bib_database))