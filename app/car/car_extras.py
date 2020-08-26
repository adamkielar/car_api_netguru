import requests


def get_cars_from_url(car_make):
    get_cars = requests.get(
        url='https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/' +
            car_make + '?format=json'
    )
    cars = get_cars.json()
    cars = cars["Results"]
    return cars
