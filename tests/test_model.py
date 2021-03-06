from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="username",
            password="password",
            first_name="Valentin",
            last_name="NotValentin",
        )

        self.assertEqual(
            str(driver), f"{driver.username} {driver.first_name} {driver.last_name}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
