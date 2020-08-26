# Car REST Api | Django REST Framework
[![Build Status](https://travis-ci.org/adamkielar/car_api_netguru.svg?branch=master)](https://travis-ci.org/adamkielar/car_api_netguru)

# Description
Django REST api to manage cars and ratings.

Deployment version on feature/deploy branch

## Endpoints

1. GET `/cars`
- List of all cars from database with current average rate.
2. POST `/cars`
- Endpoint checks posted car make and model name in external api (https://vpic.nhtsa.dot.gov/api/)
- Model name is case-sensitive
- If posted data are correct, new Car object will be created
3. GET `/popular`
- List of top cars based on number of rates
4. POST `/rate`
- Endpoint to add rate for a car from 1 to 5

# How to use:

Clone this repository.

Docker:
- `docker-compose up`
