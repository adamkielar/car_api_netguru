from django.db.models import Count

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from core.models import Car, Rating

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


class CarRatingViewSet(viewsets.ModelViewSet):
    """
    Manage following endpoint:
    POST /rate/
    """
    queryset = Rating.objects.all()
    serializer_class = serializers.CarRatingSerializer


class CarPopularViewSet(viewsets.ModelViewSet):
    """
    Manage following endpoint:
    GET /popular
    """
    allowed_methods = ['GET']
    queryset = Car.objects.all()
    serializer_class = serializers.CarPopularSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset.annotate(car_rating_count=Count('ratings')).order_by(
            '-car_rating_count')
