from .test_setup import TestSetup
from authentication.models import User


class TestViews(TestSetup):
    def test_user_cant_register_with_no_data(self):
        response = self.client.post(self.register_url)
        # assertEquals is a function to check if two variables are
        # equal, for purposes of automated testing
        self.assertEqual(response.status_code, 400)

    def test_user_can_register_successfully(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_unverified_email_user_cant_login(self):
        register = self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_verified_email_user_can_login_successfully(self):
        # register user
        register = self.client.post(self.register_url, self.user_data, format='json')

        # retrieve user instance
        user_username = register.data.get('username')
        user = User.objects.get(username=user_username)

        # manually verify user's email and save the user
        user.is_verified = True
        user.save()

        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 200)
