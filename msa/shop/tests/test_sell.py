from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.test.client import Client

from shop.models import UsableItem, Medicine, Vendor, ExpiredItem, CustomerTransaction, VendorTransaction

class SellMedicineTest(TestCase):
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
                id =id,
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

    def test_get_sell_medicine(self):
        response = self.c.get(reverse_lazy('sellmedicine'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sellmedicine.html', 'base.html')

    # all valid
    def test_post_sell_medicine1(self):
        self.sale = {
            'name': 'Customer',
            'phone': '9874563212',
            'trans': 1,
            'medicine': 1,
            'quantity': 5
        }
        response = self.c.post(reverse_lazy('sellmedicine'), data=self.sale)
        self.assertEqual(response.status_code, 200)

    def test_post_sell_medicine2(self):
        self.sale = {
            'name': 'Customer',
            'phone': '987463212',
            'trans': 1,
            'medicine': 5,
            'quantity': -5
        }
        response = self.c.post(reverse_lazy('sellmedicine'), data=self.sale)
        self.assertEqual(response.status_code, 200)

    def test_post_sell_medicine3(self):
        self.sale = {
            'name': 'Customer',
            'phone': '9874563212',
            'trans': 1,
            'medicine': 1,
            'quantity': 50000
        }
        response = self.c.post(reverse_lazy('sellmedicine'), data=self.sale)
        self.assertEqual(response.status_code, 200)

    def test_post_sell_medicine4(self):
        self.sale = {
            'name': 'Customer',
            'phone': '9874563212',
            'trans': 1,
            'medicine': 1,
            'quantity': 75
        }
        response = self.c.post(reverse_lazy('sellmedicine'), data=self.sale)
        self.assertEqual(response.status_code, 200)

    def test_get_sell_medicine4(self):
        ctr = CustomerTransaction(
            id=1,
            transaction_id=1,
            date='2021-04-04',
            expiry_date='2022-04-04',
            batch_id="87458",
            medicine=Medicine.objects.get(id=1),
            name="name",
            phone="87976451"
        )
        ctr.save()
        response = self.c.get(reverse_lazy('sellmedicine'))
        self.assertEqual(response.status_code, 200)


class PrintReceiptTest(TestCase):
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
            ctr = CustomerTransaction(
                id = id,
                transaction_id=trans,
                date='2021-04-04',
                expiry_date='2022-04-04',
                batch_id="87458",
                medicine=Medicine.objects.get(id=1),
                name="name",
                phone="87976451"
            )
            ctr.save()
        response = self.c.get(reverse_lazy(
            'printreceipt', kwargs={'trans': str(trans)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receipt.html')

    def test_print2(self):
        trans = 1
        response = self.c.post(reverse_lazy(
            'printreceipt', kwargs={'trans': str(trans)}))
        self.assertEqual(response.status_code, 302)
