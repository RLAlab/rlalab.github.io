---
title: Team
date: 2022-10-24

type: landing

sections:
  - block: people
    content:
      title: Who we are
      # Choose which groups/teams of users to display.
      #   Edit `user_groups` in each user's profile to add them to one or more of these groups.
      user_groups:
          - Principal Investigator
          - Postdoctoral Researchers
          - PhD Students
          - Staff
          - Visitors
      sort_by: Params.last_name
      sort_ascending: true
    design:
      show_interests: false
      show_role: true
      show_social: true

  - block: markdown
    content:
      title:
      subtitle:
      text: |
        {{% cta cta_link="./alumni/" cta_text="Alumni →" %}}
    design:
      columns: '1'
---