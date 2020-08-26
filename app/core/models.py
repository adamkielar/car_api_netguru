from django.db import models


class Car(models.Model):
    car_make = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)

    class Meta:
        unique_together = ['car_make', 'car_model']

    def __str__(self):
        return f'{self.car_make} {self.car_model}'


class Rating(models.Model):
    car = models.ForeignKey(Car, related_name='ratings',
                            on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.car.car_make} {self.car.car_model} rating {self.rating}'
