from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse


# Create your tests here.
class MainPageTest(APITestCase):
    def test_scraping(self):
        url = reverse("mainpage")
        response = self.client.get(url)
        # print(response["data"])
        return self.assertEqual(response.status_code, 200)
