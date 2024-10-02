---
# Leave the homepage title empty to use the site title
title:
date: 2024-09-19
type: landing

sections:
  - block: hero
    content:
      title: |
        RLA Lab
      subtitle: |
        Synthetic Biology for Metabolic Engineering
      image:
        filename: rlalab.jpeg
      text: |
        <br>
        
        The RLA Lab is interested in how the development of synthetic biology can revolutionise biotechnologies and help us to move towards a sustainable bio-based economy. We engineer microorganisms for a wide range of applications which span from the production of the chemicals and fuels we usually get from petroleum to their use in food, biomedicine and therapeutics.
  
  - block: collection
    content:
      title: Latest News
      subtitle:
      text:
      count: 5
      filters:
        author: ''
        category: ''
        exclude_featured: false
        publication_type: ''
        tag: ''
      offset: 0
      order: desc
      page_type: post
    design:
      view: card
      columns: '1'
  
  - block: markdown
    content:
      title:
      subtitle: ''
      text:
    design:
      columns: '1'
      background:
        image: 
          filename: #coders.jpg
          filters:
            brightness: 1
          parallax: false
          position: center
          size: cover
          text_color_light: true
      spacing:
        padding: ['20px', '0', '20px', '0']
      css_class: fullscreen

  - block: collection
    content:
      title: Latest Preprints
      text: ""
      count: 5
      filters:
        folders:
          - publication
        publication_type: 'article'
    design:
      view: citation
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
