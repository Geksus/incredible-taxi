from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        manufacturer2 = Manufacturer.objects.create(name="Audi", country="Germany")

        Car.objects.create(model="e32", manufacturer=manufacturer1)
        Car.objects.create(model="Q8", manufacturer=manufacturer2)

        response = self.client.get(CAR_URL)

        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(car))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_delete_car(self):
        manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        manufacturer2 = Manufacturer.objects.create(name="Audi", country="Germany")

        car1 = Car.objects.create(model="e32", manufacturer=manufacturer1)
        car2 = Car.objects.create(model="RS7", manufacturer=manufacturer2)

        self.assertEqual(Car.objects.count(), 2)

        self.client.post(reverse("taxi:car-delete", kwargs={"pk": car1.id}))
        self.client.post(reverse("taxi:car-delete", kwargs={"pk": car2.id}))

        self.assertEqual(Car.objects.count(), 0)

    def test_search_car(self):
        manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        manufacturer2 = Manufacturer.objects.create(name="Audi", country="Germany")

        Car.objects.create(model="e32", manufacturer=manufacturer1)
        Car.objects.create(model="Q8", manufacturer=manufacturer2)
        Car.objects.create(model="RS7", manufacturer=manufacturer2)
        Car.objects.create(model="e38", manufacturer=manufacturer1)

        response = self.client.get(f"{CAR_URL}?model=e")

        car = Car.objects.filter(model__icontains="e")

        self.assertEqual(list(response.context["car_list"]), list(car))


DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "HHH88888",
        }

        self.client.post(reverse("taxi:create-driver"), data=form_data)

        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
PAGINATE_BY = 2


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(MANUFACTURER_URL)

        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "BMW",
            "country": "Germany",
        }

        self.client.post(reverse("taxi:create-manufacturer"), data=form_data)

        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self):
        new_manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")

        upd_data = {"name": "Mercedes", "country": new_manufacturer.country}

        self.client.post(
            reverse("taxi:manufacturer-update", kwargs={"pk": new_manufacturer.id}),
            data=upd_data,
        )

        upd_manufacturer = Manufacturer.objects.get(pk=new_manufacturer.id)

        self.assertEqual(new_manufacturer.id, upd_manufacturer.id)
        self.assertNotEqual(new_manufacturer.name, upd_manufacturer.name)
        self.assertEqual(upd_manufacturer.name, upd_data["name"])
        self.assertEqual(new_manufacturer.country, upd_manufacturer.country)

    def test_delete_manufacturer(self):
        new_manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        new_manufacturer2 = Manufacturer.objects.create(
            name="Mercedes", country="Germany"
        )

        self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": new_manufacturer1.id})
        )
        self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": new_manufacturer2.id})
        )

        self.assertEqual(Manufacturer.objects.count(), 0)
