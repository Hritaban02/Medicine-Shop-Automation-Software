from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User, AnonymousUser
from django.test.client import Client

from shop.models import UsableItem, Medicine, Vendor, ExpiredItem, CustomerTransaction, VendorTransaction

# Abhishek
class LoginTest(TestCase):
    def setUp(self):

        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

    # login page testing
    def test_index_url(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_works_with_correct_values(self):
        response = self.client.login(username='myuser', password='mypassword')
        self.assertTrue(response)



    def test_login_fails_with_in_correct_values(self):
        response = self.client.login(username='man', password='1234@test0')
        self.assertFalse(response)


class ChangePasswordTest(TestCase):
    def setUp(self):

        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

    def test_change_password_can_be_accessed(self):
	    resp = self.client.get(reverse_lazy('change_password'))
	    self.assertEqual(resp.status_code, 302)
	    # self.assertTemplateUsed(resp, 'change-password.html', 'base.html')
	    # self.assertTemplateUsed(resp, 'base.html')

    def test_change_password_POST_with_correct_data(self):
	    self.new_password1 = "HellOfAProject"
	    self.new_password2 = "HellOfAProject"
	    self.client.force_login(self.my_admin)
	    resp = self.c.post(reverse_lazy('change_password'),
                                {'old_password': 'mypassword',
                              'new_password1': self.new_password1,
                              'new_password2': self.new_password2
                              })
	    self.assertEqual(resp.status_code, 200)

    def test_change_password_POST_with_incorrect_data(self):
	    self.new_password1 = "HellOfProject"
	    self.new_password2 = "HellOfAProject"
	    self.client.force_login(self.my_admin)
	    resp = self.c.post(reverse_lazy('change_password'),
                        {'old_password': 'mypaword',
                         'new_password1': self.new_password1,
                         'new_password2': self.new_password2
                         })
	    self.assertEqual(resp.status_code, 200)

    def test_change_password_POST_with_old_not_match(self):
	    self.new_password1 = "HellOfAProject"
	    self.new_password2 = "HellOfAProject"
	    self.client.force_login(self.my_admin)
	    resp = self.c.post(reverse_lazy('change_password'),
                        {'old_password': 'mypassword',
                         'new_password1': self.new_password1,
                         'new_password2': self.new_password2
                         })
	    self.assertEqual(resp.status_code, 200)

    def test_change_password_POST_with_old_not_match(self):
	    self.new_password1 = "HellOfAProjt"
	    self.new_password2 = "HellOfAProject"
	    self.client.force_login(self.my_admin)
	    resp = self.c.post(reverse_lazy('change_password'),
                        {'old_password': 'mypassword',
                         'new_password1': self.new_password1,
                         'new_password2': self.new_password2
                         })
	    self.assertEqual(resp.status_code, 200)
    def test_change_password_POST_with_invalid(self):
	    self.new_password1 = ""
	    self.new_password2 = ""
	    self.client.force_login(self.my_admin)
	    resp = self.c.post(reverse_lazy('change_password'),
                        {'old_password': 'mypassword',
                         'new_password1': self.new_password1,
                         'new_password2': self.new_password2
                         })
	    self.assertEqual(resp.status_code, 200)




class LogInPageTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login_correct(self):
        # send login data
        response = self.client.post('/login', self.credentials, follow=True)
        # should be logged in now
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)

    def test_login_fail(self):
        self.credentials = {
            'username': 'testuse',
            'password': 'secre'}
        # send login data
        response = self.client.post('/login', self.credentials, follow=True)
        # should be logged in now
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)


class LogOutTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.my_admin = User.objects.create_user(**self.credentials)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username='testuser', password='secret')

    def test_logout(self):
        response = self.c.post('/logout', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)

class HomeTest(TestCase):
    def setUp(self):
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.my_admin.save()
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

    def test_home(self):
        response = self.c.get(reverse_lazy(
            'home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html', 'base.html')

# <---------------------------------------------------------> #
