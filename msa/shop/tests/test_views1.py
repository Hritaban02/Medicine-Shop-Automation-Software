from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
import datetime
from shop.models import Vendor, Medicine, UsableItem


class newmedViewTest(TestCase):
	def setUp(self):
		self.vendor = Vendor.objects.create(
			name="Vendor_Name", address="Vendor_Address", phone=9876543210, email="Vendor@gmail.com")
		self.vendor.save()
		self.client = Client()
		self.username = "admin123"
		self.password = "helloworld"
		self.test = User.objects.create(
			username=self.username, password=self.password)

	def test_newmed_can_be_accessed(self):
		self.client.force_login(self.test)
		resp = self.client.get(reverse_lazy('newmed'))
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'newmed.html')
		self.assertTemplateUsed(resp, 'base.html')

	def test_newmed_POST_with_data(self):
		self.client.force_login(self.test)
		resp = self.client.post(reverse('newmed'),
                          {'trade_name': 'MedicineTradeName',
                           'generic_name': 'MedicineGenericName',
                           'description': 'MedicineDescription',
                           'purchasePrice': 9, 'unit_selling': 11,
                           'threshold_value': 5, 'vendor': self.vendor.id
                           })
		count = Medicine.objects.count()
		self.assertEqual(Medicine.objects.get(id=1).trade_name, 'MedicineTradeName')
		self.assertEqual(Medicine.objects.get(
			id=1).generic_name, 'MedicineGenericName')
		self.assertEqual(Medicine.objects.get(
			id=1).description, 'MedicineDescription')
		self.assertEqual(Medicine.objects.get(id=1).purchasePrice, 9)
		self.assertEqual(Medicine.objects.get(id=1).unit_selling, 11)
		self.assertEqual(Medicine.objects.get(id=1).threshold_value, 5)
		self.assertEqual(Medicine.objects.get(id=1).vendor, self.vendor)
		self.assertEqual(count, 1)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'newmed.html')
		self.assertTemplateUsed(resp, 'base.html')

	def test_newmed_POST_wit_no_data(self):
		self.client.force_login(self.test)
		resp = self.client.post(reverse_lazy('newmed'))
		count = Medicine.objects.count()
		self.assertEqual(count, 0)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'newmed.html')
		self.assertTemplateUsed(resp, 'base.html')


class searchViewTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.username = "admin123"
		self.password = "helloworld"
		self.test = User.objects.create(
			username=self.username, password=self.password)

	def test_search_can_be_accessed(self):
		self.client.force_login(self.test)
		resp = self.client.get(reverse_lazy('search'), {'search': ""})
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'search.html')
		self.assertTemplateUsed(resp, 'base.html')


class listOfmedViewTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.username = "admin123"
		self.password = "helloworld"
		self.test = User.objects.create(
			username=self.username, password=self.password)

	def test_listOfmed_can_be_accessed(self):
		self.client.force_login(self.test)
		resp = self.client.get(reverse_lazy('listOfMed'))
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'listOfmed.html')
		self.assertTemplateUsed(resp, 'base.html')


class below_thresholdViewTest(TestCase):
	def setUp(self):
	    self.vendor = Vendor.objects.create(name="Vendor_Name",
                                         address="Vendor_Address", phone=9876543210,    email="Vendor@gmail.com")
	    self.vendor.save()
	    self.meditem = Medicine.objects.create(trade_name='MedicineTradeName',
                                            generic_name='MedicineGenericName',     description='MedicineDescription',
                                            purchasePrice=9, unit_selling=11,   threshold_value=5, vendor=self.vendor)
	    self.meditem.save()
	    self.usableitem = UsableItem.objects.create(batch_id="1",
                                                 expiry_date=datetime.date(2022, 2,     19), order_date=datetime.date(2021,     2, 19),
                                                 quantity=50, medicine=self.meditem)
	    self.usableitem.save()
	    self.client = Client()
	    self.username = "admin123"
	    self.password = "helloworld"
	    self.test = User.objects.create(
                username=self.username, password=self.password)

	def test_below_threshold_can_be_accessed(self):
		self.client.force_login(self.test)
		resp = self.client.get(reverse_lazy('below_threshold'))
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'below_threshold.html')