from django.db import IntegrityError
from django.test import TestCase

from core import models


class ModelTest(TestCase):

    def setUp(self):
        self.car1 = models.Car.objects.create(
            car_make='Nissan',
            car_model='GT-R',
        )

    def test_car_str(self):
        """Test car object string representation"""
        car = models.Car.objects.create(
            car_make='Audi',
            car_model='RS6',
        )

        self.assertEqual(
            str(car),
            f'{car.car_make} {car.car_model}'
        )

    def test_car_make_model_unique(self):
        """Test that car make and model are unique"""
        models.Car.objects.create(
            car_make='Skoda',
            car_model='Kodiaq',
        )

        with self.assertRaises(IntegrityError):
            models.Car.objects.create(
                car_make='Skoda',
                car_model='Kodiaq',
            )

    def test_car_rating_str(self):
        """Test car rating string representation"""
        car_rating = models.Rating.objects.create(
            car=self.car1,
            rating=5
        )

        self.assertEqual(
            str(car_rating),
            f'{self.car1.car_make} {self.car1.car_model} '
            f'rating {car_rating.rating}'
        )
