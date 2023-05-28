from django.urls import path

from rest_framework import routers

from search_service.views import CreateCargoView, CargoListView, CarUpdateView, CargoViewSet

app_name = 'search_service'

router = routers.SimpleRouter()
router.register(r'cargo', CargoViewSet, basename='cargo')

urlpatterns = [
    path('create-cargo/', CreateCargoView.as_view(), name='create_cargo'),
    path('cargos/', CargoListView.as_view(), name='cargos_list'),
    path('car-update/<str:uid>/', CarUpdateView.as_view(), name='car_update')
]


urlpatterns += router.urls
