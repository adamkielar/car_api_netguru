from django.db import models


class Car(models.Model):
    car_make = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ['car_make', 'car_model']

    def __str__(self):
        return f'{self.car_make} {self.car_model}'
