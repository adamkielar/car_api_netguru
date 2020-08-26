from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Car, Rating

from car.serializers import CarListSerializer, CarAddSerializer, \
    CarRatingSerializer, CarPopularSerializer

CARS_URL = reverse('car:car-list')
CARS_POPULAR_URL = reverse('car:rating-popular')
CARS_RATING_URL = reverse('car:rate-list')


def detail_url(car_id):
    """Return car detail URL"""
    return reverse('car:car-detail', args=[car_id])


class CarApiTest(TestCase):
    """Test car api"""

    def setUp(self):
        self.client = APIClient()
        self.car1 = Car.objects.create(
            car_make='Nissan',
            car_model='Juke',
        )
        self.car2 = Car.objects.create(
            car_make='Fiat',
            car_model='Panda',
        )

    def test_retrieve_cars(self):
        """Test retrieving a list of cars"""
        response = self.client.get(CARS_URL)

        cars = Car.objects.all()
        serializer = CarListSerializer(cars, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_car_success(self):
        """Test creating car"""
        payload = {
            'car_make': 'Nissan',
            'car_model': 'Altra',
        }
        self.client.post(CARS_URL, payload)

        exists = Car.objects.filter(
            car_make=payload['car_make'],
            car_model=payload['car_model']
        ).exists()
        self.assertTrue(exists)

    def test_create_car_invalid(self):
        """Test creating car with invalid payload"""
        payload = {'car_make': 'empty'}
        response = self.client.post(CARS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_view_detail(self):
        """Test viewing a car rate detail"""
        car = self.car1
        url = detail_url(car.id)

        response = self.client.get(url)
        serializer = CarRatingSerializer(car)

        self.assertEqual(response.data, serializer.data)

    def test_retrieve_popular_cars(self):
        """Test retrieving a list of popular cars by number of rates"""
        response = self.client.get(CARS_POPULAR_URL)

        cars = Car.objects.all()
        serializer = CarPopularSerializer(cars, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
