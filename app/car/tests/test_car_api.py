from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Car, Rating

from car.serializers import CarListSerializer, CarRatingSerializer

CARS_URL = reverse('car:car-list')
CARS_POPULAR_URL = reverse('car:popular-list')
CARS_RATING_URL = reverse('car:rate-list')


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
        self.car3 = Car.objects.create(
            car_make='BMW',
            car_model='M4',
        )
        self.rating1 = Rating.objects.create(
            car=self.car1,
            rating=5
        )
        self.rating2 = Rating.objects.create(
            car=self.car1,
            rating=5
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

    def test_retrieve_cars_with_average_rating(self):
        """Test retrieving a list of cars with average rating"""
        response = self.client.get(CARS_URL)
        cars = Car.objects.all()
        CarListSerializer(cars, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['average_rating'], 5.0)

    def test_rate_view(self):
        """Test viewing a car rate view"""
        response = self.client.get(CARS_RATING_URL)

        car_ratings = Rating.objects.all()
        serializer = CarRatingSerializer(car_ratings, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_car_rate_create(self):
        """Test updating car rating"""
        car = self.car3

        payload = {
            'car': [car.id],
            'rating': 5
        }
        self.client.post(CARS_RATING_URL, payload)

        exists = Rating.objects.filter(
            car=self.car1,
            rating=payload['rating']
        ).exists()
        self.assertTrue(exists)

    def test_retrieve_popular_cars(self):
        """Test retrieving a list of popular cars"""
        response = self.client.get(CARS_POPULAR_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
