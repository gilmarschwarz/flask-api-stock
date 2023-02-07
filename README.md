# Flask API

## Description
This project is designed of back-end, specifically in the Flask framework, Rest APIs, and decoupled services (microservices).

## Assignment
The goal of this project is to create a simple API using Flask to allow users to query [stock quotes]

The project consists of two separate services:
* A user-facing API that received requests from registered users asking for quote information.
* An internal stock aggregator service that queries external APIs to retrieve the requested quote information.

## Architecture
1. A user makes a request asking for Apple's current Stock quote: `GET /stock?q=aapl.us`
2. The API service calls the stock service to retrieve the requested stock information
3. The stock service delegates the call to the external API, parses the response, and returns the information back to the API service.
4. The API service saves the response from the stock service in the database.
5. The data is formatted and returned to the user.
6. A super user can hit the stats endpoint, which will return the top 5 most requested stocks

## How to run the project
* Create a virtualenv: `python -m venv virtualenv` and activate it `. virtualenv/bin/activate`.
* Install dependencies: `pip install -r requirements.txt`
* Start the api service: `cd api_service ; flask db migrate; flask db upgrade ; flask run`
* Start the stock service: `cd stock_service ; flask run`
* This project use Oracle DataBase, so the tables must have a sequence defined in "id" column for USER and HISTORY when the tables are created. In `extensions.py`, an instant client installed must be setted