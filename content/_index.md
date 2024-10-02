---
# Leave the homepage title empty to use the site title
title:
date: 2024-09-19
type: landing

sections:
  - block: hero
    content:
      title: |
        RLA Lab <br>
      subtitle: |
        **Synthetic Biology for Metabolic Engineering**
      image:
        filename: rlalab.jpeg
      text: |
        **Synthetic Biology for Metabolic Engineering**
        <br> <br>

        The RLA Lab is interested in how the development of synthetic biology can revolutionise biotechnologies and help us to move towards a sustainable bio-based economy. We engineer microorganisms for a wide range of applications which span from the production of the chemicals and fuels we usually get from petroleum to their use in food, biomedicine and therapeutics.
    
  - block: collection
    content:
      title: Latest publications
      text: ""
      count: 5
      filters:
        folders:
          - publication
        publication_type: 'article-journal'
      sort_by: 'Date'
    design:
      view: list
      columns: '1'

  - block: markdown
    content:
      title:
      subtitle:
      text: |
        {{% cta cta_link="./people/" cta_text="Meet the team →" %}}
    design:
      columns: '1'
---
