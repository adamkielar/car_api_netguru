from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from core.models import Car

from car import serializers
from car.car_extras import get_cars_from_url


class CarViewSet(viewsets.ModelViewSet):
    """
    Manage following endpoint:
    GET /cars
    POST /cars
    """
    allowed_methods = ['GET', 'POST']
    queryset = Car.objects.all()
    serializer_class = serializers.CarListSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'create':
            return serializers.CarAddSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        car_make = str(self.request.data.get('car_make'))
        car_model = str(self.request.data.get('car_model'))

        cars = get_cars_from_url(car_make)
        if cars:
            for car in cars:
                if car_model == car['Model_Name']:
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED,
                                    headers=headers)
            return Response(
                {'message': 'Car Model do not exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'message': 'Car Make do not exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
