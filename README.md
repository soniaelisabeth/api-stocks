<div align="center">
    <img src="https://raw.githubusercontent.com/Jobsity/ReactChallenge/main/src/assets/jobsity_logo_small.png"/>
</div>

# Flask Challenge

## Project's Changes

1. To make things easier, a Postman workspace was used and recommended to authenticate and validate the endpoints.
2. To work with the process validation, notice that is necessary to execute the API endpoint 'login', once you already have the users on the database.
3. It's also necessary to get the 'login' endpoint's return and add to the API calls, on Postman, on the Headers of a call:
Key: Authorization
Value: Bearer (insert here the api login's return)
![1](./helper_imgs/1.png)

4. Please notice that the requirements.txt was updated with all the libs and versions I used in this test. I left the versions because I also think it's important on a project, thus the biggest change was the Flask JWT lib.
5. My biggest challenge was the connection with SQLAlchemy, which I could not make it work due to an error that keep occurring with the key SQLALCHEMY_DATABASE_URI. I believe this was my only failure on this project, but I could make everything work with the simple lib sqlite3. Also, please remember to change the MAIN_DB_PATH sql_util file, to the full path if needed.

## Populate the databases
- The User (and the Stocks) tables are going to be CREATED in the api_service database when running flask db migrate; flask db upgrade
- Please make sure that the program used the migrations/versions' python file to create the tables.
- The User database is going to be POPULATED when navigating to the api_service folder, in the CMD running "python manager.py init". This adds the default allowed users to the User table.
- The Stocks database is going to be POPULATED only when the "/stock" endpoint is called.

## Considerations

The project was a challenge that I really enjoyed doing I made the hard decision to work with something I was already fammiliar with when dealing with the databases processes, also because of the due date. I believe choices like this are supposed to be made on a programmer's daily basis, always paying attention on the due date outcome and making the decision on what to spend your time on.
If more time is provided I would love to implement more of the extras requirements and studying more about the SqlAlchemy issue.

Thank you for the opportunity!

## Changes I Would Like to Make

- Add a Swagger file for the API
- Add tests
- Working better with the Schema classes
- Working with SqlAlchemy
- Making functions more readble


## Description
This project is designed to test your knowledge of back-end web technologies, specifically in the Flask framework, Rest APIs, and decoupled services (microservices).

## Assignment
The goal of this exercise is to create a simple API using Flask to allow users to query [stock quotes](https://www.investopedia.com/terms/s/stockquote.asp).

The project consists of two separate services:
* A user-facing API that will receive requests from registered users asking for quote information.
* An internal stock aggregator service that queries external APIs to retrieve the requested quote information.

For simplicity, both services will share the same dependencies (requirements.txt) and can be run from the same virtualenv, but remember that they are still separate processes.

## Minimum requirements
### API service
* Endpoints in the API service should require authentication (no anonymous requests should be allowed). Each request should be authenticated via Basic Authentication.
You have to implement the code to check the user credentials are correct and put the right decorators around resource methods (check the auth.helpers module).
* When a user makes a request to get a stock quote (calls the stock endpoint in the api service), if a stock is found, it should be saved in the database associated to the user making the request.
* The response returned by the API service should be like this:

  `GET /stock?q=aapl.us`
  ```
    {
    "symbol": "AAPL.US",
    "company_name": "APPLE",
    "quote": 123
    }
  ```
  The quote value should be taken from the `close` field returned by the stock service.
* A user can get his history of queries made to the api service by hitting the history endpoint. The endpoint should return the list of entries saved in the database, showing the latest entries first:
  
  `GET /history`
  ```
  [
      {"date": "2021-04-01T19:20:30Z", "name": "APPLE", "symbol": "AAPL.US", "open": "123.66", "high": 123.66, "low": 122.49, "close": "123"},
      {"date": "2021-03-25T11:10:55Z", "name": "APPLE", "symbol": "AAPL.US", "open": "121.10", "high": 123.66, "low": 122, "close": "122"},
      ...
  ]
  ```
* A super user (and only super users) can hit the stats endpoint, which will return the top 5 most requested stocks:

  `GET /stats`
  ```
  [
      {"stock": "aapl.us", "times_requested": 5},
      {"stock": "msft.us", "times_requested": 2},
      ...
  ]
  ```
* All endpoint responses should be in JSON format.

### Stock service
* Assume this is an internal service, so requests to endpoints in this service don't need to be authenticated.
* When a stock request is received, this service should query an external API to get the stock information. For this challege, use this API: `https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv`.
* Note that `{stock_code}` above is a parameter that should be replaced with the requested stock code.
* You can see a list of available stock codes here: https://stooq.com/t/?i=518

## Architecture
![Architecture Diagram](diagram.svg)
1. A user makes a request asking for Apple's current Stock quote: `GET /stock?q=aapl.us`
2. The API service calls the stock service to retrieve the requested stock information
3. The stock service delegates the call to the external API, parses the response, and returns the information back to the API service.
4. The API service saves the response from the stock service in the database.
5. The data is formatted and returned to the user.

## Bonuses
The following features are optional to implement, but if you do, you'll be ranked higher in our evaluation process.
* Add unit tests for the bot and the main app.
* Connect the two services via RabbitMQ instead of doing http calls.
* Use JWT instead of basic authentication for endpoints.

## How to run the project
* Create a virtualenv: `python -m venv virtualenv` and activate it `. virtualenv/bin/activate`.
* Install dependencies: `pip install -r requirements.txt`
* Start the api service: `cd api_service ; flask db migrate; flask db upgrade ; flask run`
* Start the stock service: `cd stock_service ; flask run`

__Important:__ If your implementation requires different steps to start the services
(like starting a rabbitMQ consumer), document them here!

