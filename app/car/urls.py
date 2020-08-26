from rest_framework.routers import SimpleRouter

from car import views

app_name = 'car'

router = SimpleRouter()
router.register('cars', views.CarViewSet)
router.register('popular', views.CarPopularViewSet)
router.register('rate', views.CarRatingViewSet)

urlpatterns = router.urls
