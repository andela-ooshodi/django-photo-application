from django.test import TestCase, Client
from django.contrib.auth.models import User
from photoapp.models import UserProfile


class AuthenticationTestClass(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            password='tester',
        )
        self.profile = UserProfile.objects.get_or_create(user=self.user)[0]
        self.profile.photo = "https://sampleurotoprofileimage"
        self.profile.save

    def test_can_reach_login_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'photoapp/login.html')

    def test_confirm_logged_in(self):
        login = self.client.login(username='test', password='tester')
        self.assertTrue(login)
        response = self.client.get('/')
        # redirects a logged in user
        self.assertEqual(response.status_code, 302)

    def test_unauthorized_access(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 302)

    def test_can_reach_home_page(self):
        self.client.login(username='test', password='tester')
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'photoapp/home.html')
