from rest_framework.test import APITestCase
from django.urls import reverse

"""
The setUp() and tearDown() methods allow you to 
define instructions that will be executed before 
and after each test method. 
"""


class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.user_data = {
            'username': 'username12',
            'email': 'email@example.com',
            'password': 'passvvordtest',
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
