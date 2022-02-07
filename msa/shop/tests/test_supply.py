from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.test.client import Client

from shop.models import UsableItem, Medicine, Vendor, ExpiredItem, CustomerTransaction, VendorTransaction


class NewSupplyMedTest(TestCase):
    @classmethod
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
                vendor=Vendor.objects.get(id=1)
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
        test = UsableItem.objects.create(
            id=3,
            batch_id="test_batch",
            expiry_date="2035-04-04",
            order_date="2021-05-04",
            quantity=50,
            medicine=Medicine.objects.get(id=1)
        )
        test.save()

        self.username = 'my_admin'
        self.password = '1234@test'

    def test_get_new_supplymed(self):
        response = self.c.get(reverse_lazy(
            'newsupplymed', kwargs={'id': "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsupplymed.html', 'base.html')

    

    def test_get_new_supplymed1(self):
        vtr = VendorTransaction(
            id=1,
            transaction_id=1,
            date='2021-04-04',
            expiry_date='2022-04-04',
            batch_id="87458",
            medicine=Medicine.objects.get(id=1),
            vendor=Vendor.objects.get(id=1)
        )
        vtr.save()
        response = self.c.get(reverse_lazy(
            'newsupplymed', kwargs={'id': "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsupplymed.html', 'base.html')

    def test_post_new_supplymed(self):
        self.sale = {
            'name': 'vendor',
            'medicine': 1,
            'batch_id': '63212',
            'order_date': '2021-04-04',
            'expiry_date': '2022-04-04',
            'trans': -1,
            'quantity': -5
        }
        response = self.c.post(reverse_lazy(
            'newsupplymed', kwargs={'id': "1"}), data=self.sale)
        self.assertEqual(response.status_code, 200)

    def test_post_new_supplymed1(self):
        self.sale = {
            'medicine': 1,
            'batch_id': 'adfadf',
            'order_date': '2022-04-04',
            'expiry_date': '2022-06-04',
            'trans': 1,
            'quantity': 5
        }
        response = self.c.post(reverse_lazy(
            'newsupplymed', kwargs={'id': "1"}), data=self.sale)
        self.assertEqual(response.status_code, 200)

    def test_post_new_supplymed2(self):
        self.sale = {
            'name': 'vendor',
            'medicine': 1,
            'batch_id': '63212',
            'order_date': '2021-04-04',
            'expiry_date': '2022-04-04',
            'trans': -1,
            'quantity': -5
        }
        Medicine.objects.all().delete()
        response = self.c.post(reverse_lazy(
            'newsupplymed', kwargs={'id': "1"}), data=self.sale)
        self.assertEqual(response.status_code, 200)
    


class PrintVendorReceiptTest(TestCase):
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
        test = UsableItem.objects.create(
            id=3,
            batch_id="test_batch",
            expiry_date="2035-04-04",
            order_date="2021-05-04",
            quantity=50,
            medicine=Medicine.objects.get(id=1)
        )
        test.save()

        self.username = 'my_admin'
        self.password = '1234@test'

    def test_print(self):
        trans = 1
        for id in range(1, 5):
            vtr = VendorTransaction(
                id=id,
                transaction_id=trans,
                date='2021-04-04',
                expiry_date='2022-04-04',
                batch_id="87458",
                medicine=Medicine.objects.get(id=1),
                vendor=Vendor.objects.get(id=1)
            )
            vtr.save()
        response = self.c.get(reverse_lazy(
            'printvendorreceipt', kwargs={'trans': str(trans)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendorreceipt.html')

    def test_print2(self):
        trans = 1
        response = self.c.post(reverse_lazy(
            'printvendorreceipt', kwargs={'trans': str(trans)}))
        self.assertEqual(response.status_code, 302)


class NewSupply(TestCase):
    def setUp(self):
        num_vendor = 5
        for id in range(1, num_vendor):
            test = Vendor(
                id,
                f"test{id}",
                f"test{id} address",
                f"987654321{id}",
                f"test{id}@email.com"
            )
            test.save()
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

    def test_newsupply(self):
        response = self.c.get(reverse_lazy(
            'newsupply'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsupply.html', 'base.html')
    
