from shop.models import Transaction, UsableItem, Medicine, Vendor, ExpiredItem, CustomerTransaction, VendorTransaction
from django.test.client import Client
from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from shop.views import threshold, usable


class UsableTest(TestCase):
    def setUp(self):
        num_vendor = 3
        num_medicine = 3
        num_usable_item = 3
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

        for id in range(1, num_vendor):
            test = Vendor(
                id,
                f"test{id}",
                f"test{id} address",
                f"987654321{id}",
                f"test{id}@email.com"
            )
            test.save()
        for id in range(1, num_medicine):
            test = Medicine(
                id=id,
                trade_name=f"test_trade{id}",
                generic_name=f"test_generic{id}",
                description=f"description{id}",
                purchasePrice=50.0,
                unit_selling=60.0,
                threshold_value=10,
                vendor=Vendor.objects.get(id=id)
            )
            test.save()
        for id in range(1, num_usable_item):
            test = UsableItem.objects.create(
                id=id,
                batch_id=f"test_batch{id}",
                expiry_date="2025-04-04",
                order_date="2021-04-04",
                quantity=50,
                medicine=Medicine.objects.get(id=id)
            )
            test.save()

        self.username = 'my_admin'
        self.password = '1234@test'

    def test_get_usable(self):
        response = self.c.get(reverse_lazy('usable'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usable.html', 'base.html')

    def test_post_usable(self):

        response = self.c.post(reverse_lazy('usable'))
        self.assertEqual(response.status_code, 200)


class ExpiredTest(TestCase):
    def setUp(self):
        num_vendor = 3
        num_medicine = 3
        num_usable_item = 3
        num_expired_item = 3
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

        for id in range(1, num_vendor):
            test = Vendor(
                id,
                f"test{id}",
                f"test{id} address",
                f"987654321{id}",
                f"test{id}@email.com"
            )
            test.save()
        for id in range(1, num_medicine):
            test = Medicine(
                id=id,
                trade_name=f"test_trade{id}",
                generic_name=f"test_generic{id}",
                description=f"description{id}",
                purchasePrice=50.0,
                unit_selling=60.0,
                threshold_value=10,
                vendor=Vendor.objects.get(id=id)
            )
            test.save()
        for id in range(1, num_usable_item):
            test = UsableItem.objects.create(
                id=id,
                batch_id=f"test_batch{id}",
                expiry_date="2025-04-04",
                order_date="2021-04-04",
                quantity=50,
                medicine=Medicine.objects.get(id=id)
            )
            test.save()
        for id in range(1, num_expired_item):
            test = ExpiredItem(
                id=id,
                batch_id=f"test_batch{id}",
                expiry_date="2021-08-08",
                order_date="2020-04-04",
                quantity=50,
                medicine=Medicine.objects.get(id=id)
            )
            test.save(force_insert=True)
        self.username = 'my_admin'
        self.password = '1234@test'

    def test_get_expired(self):
        response = self.c.get(reverse_lazy('expired'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expired.html', 'base.html')

    def test_post_expired(self):

        response = self.c.post(reverse_lazy('expired'))
        self.assertEqual(response.status_code, 200)


class Clear_exp_Test(TestCase):
    def setUp(self):
        num_vendor = 3
        num_medicine = 3
        num_usable_item = 3
        num_expired_item = 3
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

        for id in range(1, num_vendor):
            test = Vendor(
                id,
                f"test{id}",
                f"test{id} address",
                f"987654321{id}",
                f"test{id}@email.com"
            )
            test.save()
        for id in range(1, num_medicine):
            test = Medicine(
                id=id,
                trade_name=f"test_trade{id}",
                generic_name=f"test_generic{id}",
                description=f"description{id}",
                purchasePrice=50.0,
                unit_selling=60.0,
                threshold_value=10,
                vendor=Vendor.objects.get(id=id)
            )
            test.save()

        for id in range(1, num_expired_item):
            test = ExpiredItem(
                id=id,
                batch_id=f"test_batch{id}",
                expiry_date="2026-08-08",
                order_date="2021-04-04",
                quantity=50,
                medicine=Medicine.objects.get(id=id)
            )
            test.save(force_insert=True)
        self.username = 'my_admin'
        self.password = '1234@test'

    def test_get_clear_exp(self):
        response = self.c.get(reverse_lazy('clear_exp'))
        self.assertEqual(response.status_code, 302)

    def test_post_clear_exp(self):

        response = self.c.post(reverse_lazy('clear_exp'))
        self.assertEqual(response.status_code, 302)


class Addvendor_Test(TestCase):
    def setUp(self):
        num_vendor = 3
        num_medicine = 3
        num_usable_item = 3
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

        for id in range(1, num_vendor):
            test = Vendor(
                id,
                f"test{id}",
                f"test{id} address",
                f"987654321{id}",
                f"test{id}@email.com"
            )
            test.save()
        for id in range(1, num_medicine):
            test = Medicine(
                id=id,
                trade_name=f"test_trade{id}",
                generic_name=f"test_generic{id}",
                description=f"description{id}",
                purchasePrice=50.0,
                unit_selling=60.0,
                threshold_value=10,
                vendor=Vendor.objects.get(id=id)
            )
            test.save()
        for id in range(1, num_usable_item):
            test = UsableItem.objects.create(
                id=id,
                batch_id=f"test_batch{id}",
                expiry_date="2025-04-04",
                order_date="2021-04-04",
                quantity=50,
                medicine=Medicine.objects.get(id=id)
            )
            test.save()

        self.username = 'my_admin'
        self.password = '1234@test'

    def test_get_Addvendor(self):
        response = self.c.get(reverse_lazy('addvendor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addvendor.html', 'base.html')

    def test_post_test_get_Addvendor(self):

        self.ven1 = {
            'name': 'Vendor_X',
            'address': 'Vendor_X_add',
            'phone': '1234567890',
            'email': 'Vendor_X@email.com'
        }
        self.ven2 = {
            'name': 'Vendor_X',
            'address': 'Vendor_X_add',
            'phone': '1234567',
            'email': 'Vendor_X@email.com'
        }

        response = self.c.post(reverse_lazy('addvendor'), data=self.ven1)
        response = self.c.post(reverse_lazy('addvendor'), data=self.ven2)
        self.assertEqual(response.status_code, 200)


class Threshold_Test(TestCase):
    def setUp(self):
        num_vendor = 3
        num_medicine = 3
        num_usable_item = 3
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

        for id in range(1, num_vendor):
            test = Vendor(
                id,
                f"test{id}",
                f"test{id} address",
                f"987654321{id}",
                f"test{id}@email.com"
            )
            test.save()
        for id in range(1, num_medicine):
            test = Medicine(
                id=id,
                trade_name=f"test_trade{id}",
                generic_name=f"test_generic{id}",
                description=f"description{id}",
                purchasePrice=50.0,
                unit_selling=60.0,
                threshold_value=10,
                vendor=Vendor.objects.get(id=id)
            )
            test.save()
        for id in range(1, num_usable_item):
            test = UsableItem.objects.create(
                id=id,
                batch_id=f"test_batch{id}",
                expiry_date="2025-04-04",
                order_date="2021-04-04",
                quantity=50,
                medicine=Medicine.objects.get(id=id)
            )
            test.save()

            test = CustomerTransaction.objects.create(
                name="name1",
                phone="1234567890",
                transaction_id="1",
                quantity="1",
                date="2021-04-04",
                expiry_date="2025-04-04",
                batch_id="2",
                medicine=Medicine.objects.get(id=1)
            )

        self.username = 'my_admin'
        self.password = '1234@test'

    def test_get_Threshold(self):
        response = self.c.get(reverse_lazy('threshold'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'threshold.html', 'base.html')

    def test_post_test_get_Threshold(self):

        response = self.c.post(reverse_lazy('threshold'))
        self.assertEqual(response.status_code, 200)


class Revenue_Test(TestCase):
    def setUp(self):
        num_vendor = 3
        num_medicine = 3
        num_usable_item = 3
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

        for id in range(1, num_vendor):
            test = Vendor(
                id,
                f"test{id}",
                f"test{id} address",
                f"987654321{id}",
                f"test{id}@email.com"
            )
            test.save()
        for id in range(1, num_medicine):
            test = Medicine(
                id=id,
                trade_name=f"test_trade{id}",
                generic_name=f"test_generic{id}",
                description=f"description{id}",
                purchasePrice=50.0,
                unit_selling=60.0,
                threshold_value=10,
                vendor=Vendor.objects.get(id=id)
            )
            test.save()
        for id in range(1, num_usable_item):
            test = UsableItem.objects.create(
                id=id,
                batch_id=f"test_batch{id}",
                expiry_date="2025-04-04",
                order_date="2021-04-04",
                quantity=50,
                medicine=Medicine.objects.get(id=id)
            )
            test.save()

        for id in range(1, num_usable_item):
            test = CustomerTransaction.objects.create(
                name="name1",
                phone="1234567890",
                transaction_id="1",
                quantity="1",
                date="2021-04-04",
                expiry_date="2025-04-04",
                batch_id="2",
                medicine=Medicine.objects.get(id=1)
            )

        test2 = VendorTransaction.objects.create(
            transaction_id="1",
            medicine_id="1",
            vendor=Vendor.objects.get(id=1)
        )

        self.username = 'my_admin'
        self.password = '1234@test'

    def test_get_Revenue(self):
        response = self.c.get(reverse_lazy('revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revenue.html', 'base.html')

    def test_post_test_get_Revenue(self):

        self.date = {
            'start_date': '2021-04-04',
            'end_date': '2025-04-04'
        }
        self.date2 = {
            'start_date': '2022-04-04',
            'end_date': '2025-04-44'
        }

        response = self.c.post(reverse_lazy('revenue'), data=self.date)
        response = self.c.post(reverse_lazy('revenue'), data=self.date2)
        self.assertEqual(response.status_code, 200)
