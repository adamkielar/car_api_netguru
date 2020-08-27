from django.urls import path
from django.shortcuts import redirect
from rest_framework.routers import SimpleRouter

from car import views

app_name = 'car'

router = SimpleRouter()
router.register('cars', views.CarViewSet)
router.register('popular', views.CarPopularViewSet, basename='popular')
router.register('rate', views.CarRatingViewSet, basename='rate')

urlpatterns = [
    path('', lambda request: redirect('cars/', permanent=False))
]

urlpatterns += router.urls
