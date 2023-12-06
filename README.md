# AI News

## Description

This is an implementation of ChatGPT functionality in a news website.
The web application is implemented in Django and uses the OpenAI API to query a model about published articles.

The application contains the following main files:

- kenyans app
  - views.py - Contains application logic that renders the different web pages and interfaces with the OpenAI API.
  - models.py - Contains models defining database schemas for the website.
  - urls.py - Contains urls for accessing the different app routes.
- static folder
  - styles.css - Contains styling for the application
- templates folder
  - layout.html - Contains the base layout for the web pages.
  - index.html - Contains the structure of the landing page.
  - article_detail.html - Contains the individual articles.
  - write.html - Contains the page for saving an article.
  - fill.html - Contains the page for interacting with ChatGPT.
- assistant.json - File that stores an assistant ID for a saved model.
- articles.txt - File that stores articles as they are saved into the database.

## Getting Started

This is a sample web app accessed through its URL.
