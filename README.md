# graphql-query-web-viewer
A PoC Python Web application using Flask to view as chart the output of a GraphQL API query
This code use the .env file to store the bearer token, remember to create this file and add it to your local .gitgnore

First, install Flask, Plotly, Requests and Dotenv: pip install flask requests plotly python_dotenv
Then setup the app and Flask with:
set FLASK_APP=app
flask run
