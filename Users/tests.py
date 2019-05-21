from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.test import APITestCase

User = get_user_model()


class UserRegisterLogin(APITestCase):

    def setUp(self):
        self.code = '123456'
        self.phone_number = '17600645009'
        self.password = 'admin123'
        self.password_new = 'admin1234'
        self.register_send_message()
        self.register_user()
        self.change_password_send_message()
        self.login_send_message()

    def register_send_message(self):
        sms_url = reverse('code')
        data = {"phone_number": self.phone_number, 'purpose': 0}
        response = self.client.post(sms_url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def register_user(self):
        register_url = reverse('register')
        data = {'code': self.code, 'phone_number': self.phone_number, 'password': self.password}
        response = self.client.post(register_url, data=data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.json().get('username'), '17600645009')

        return response.json().get('username')

    def test_login_with_password(self):
        login_password_url = reverse('login_password')
        data = {'phone_number': self.phone_number, 'password': self.password}
        response = self.client.post(login_password_url, data=data, format='json')

        self.assertEqual(response.status_code, 200)

    def change_password_send_message(self):
        sms_url = reverse('code')
        data = {"phone_number": self.phone_number, 'purpose': 2}
        response = self.client.post(sms_url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_change_password(self):
        user = User.objects.first()
        self.client.login(username=self.phone_number, password=self.password)
        change_password_url = reverse('change_password', kwargs={'pk': user.id})
        data = {'code': self.code, 'old_password': self.password, 'new_password': self.password_new}
        response = self.client.put(change_password_url, data=data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(authenticate(username=user.username, password=self.password), None)
        self.assertEqual(authenticate(username=user.username, password=self.password_new), user)

    def login_send_message(self):
        sms_url = reverse('code')
        data = {"phone_number": self.phone_number, 'purpose': 1}
        response = self.client.post(sms_url, data=data, format='json')

        self.assertEqual(response.status_code, 201)

    def test_login_with_smscode(self):
        login_sms_url = reverse('login_smscode')
        data = {'code': self.code, 'phone_number': self.phone_number}
        response = self.client.post(login_sms_url, data=data, format='json')

        self.assertEqual(response.status_code, 200)