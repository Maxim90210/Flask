from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Package


class PackageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.package = Package.objects.create(
            name="Test Package",
            description="A test package for the user",
            owner=self.user,
            tracking_number="123456789"
        )

    def test_get_package(self):
        """
        Тест отримання посилки користувачем через API або view
        """
        self.client.login(username='testuser', password='testpass')

        url = reverse('package-detail', kwargs={'tracking_number': self.package.tracking_number})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test Package")
        self.assertContains(response, "A test package for the user")
        self.assertContains(response, self.package.tracking_number)

    def test_package_model(self):
        """
        Тест перевірки моделі посилки
        """
        self.assertEqual(self.package.name, "Test Package")
        self.assertEqual(self.package.description, "A test package for the user")
        self.assertEqual(self.package.owner, self.user)
        self.assertEqual(self.package.tracking_number, "123456789")

    def test_unauthenticated_package_access(self):
        """
        Тест, щоб перевірити, чи користувач без авторизації не може отримати доступ до посилки
        """
        url = reverse('package-detail', kwargs={'tracking_number': self.package.tracking_number})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
