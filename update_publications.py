
from scholarly import scholarly
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

# Function to create a BibTeX entry from a publication dictionary
def create_bibtex_entry(publication):
    # Create a dictionary in BibTeX format
    bib_entry = {
        "ENTRYTYPE": "article",
        "ID": publication.get('author_pub_id', 'unknown_id'),
        "title": publication['bib'].get('title', ''),
        "author": publication['bib'].get('author', ''),
        "journal": publication['bib'].get('citation', '').split(",")[0],
        "volume": publication['bib'].get('volume', ''),
        "number": publication['bib'].get('number', ''),
        "pages": publication['bib'].get('pages', ''),
        "year": str(publication['bib'].get('pub_year', '')),
        "publisher": publication['bib'].get('publisher', ''),
        "url": publication.get('pub_url', '')
    }
    return bib_entry

# Get Google Scholar profile
search_query = scholarly.search_author('Rodrigo Ledesma-Amaro')
author = scholarly.fill(next(search_query))

# Generate BibTeX for publications
bibtex_entries = []
for pub in author['publications']:
    publication = scholarly.fill(pub)
    bibtex_entry = create_bibtex_entry(publication)
    bibtex_entries.append(bibtex_entry)

# Create BibTeX database
bib_database = BibDatabase()
bib_database.entries = bibtex_entries

# Convert the BibTeX database to a BibTeX string
writer = BibTexWriter()
bibtex_string = writer.write(bib_database)

# Save to file
with open("publications.bib", "w") as bibtex_file:
    bibtex_file.write(bibtex_string)

print("BibTeX file created successfully.")

