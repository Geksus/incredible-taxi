from django.urls import path

from .views import (
    index,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView,
    CarCreateView,
    CarUpdateView,
    CarDeleteView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    ManufacturerCreateView,
    DriverCreateView,
    DriverUpdateView,
    DriverDeleteView,
    register_request,
)

urlpatterns = [
    path("", index, name="index"),
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"),
    path("create-car/", CarCreateView.as_view(), name="create-car"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path(
        "manufacturers/<int:pk>/update/",
        ManufacturerUpdateView.as_view(),
        name="manufacturer-update",
    ),
    path(
        "manufacturers/<int:pk>/delete/",
        ManufacturerDeleteView.as_view(),
        name="manufacturer-delete",
    ),
    path(
        "manufacturers/create/",
        ManufacturerCreateView.as_view(),
        name="create-manufacturer",
    ),
    path("drivers/create/", DriverCreateView.as_view(), name="create-driver"),
    path("drivers/<int:pk>/update/", DriverUpdateView.as_view(), name="driver-update"),
    path("drivers/<int:pk>/delete", DriverDeleteView.as_view(), name="driver-delete"),
    path("register/", register_request, name="register"),
]

app_name = "taxi"
