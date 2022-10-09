import json
from wsgiref import headers
from django.test import TestCase
import requests


class LegalPolicyTestCase(TestCase):

    def setUp(self) -> None:
        self.client = requests
        self.base_url = "http://127.0.0.1:8000/api/"
        self.headers={
            "Content-Type": "application/json"
        }
        self.new_app_data = {
            "platform_type": "App",
            "app_or_website_or_service_name": "Sample",
            "app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies",
            "description": "App description",
            "company_name": "Dowell",
            "company_address": "Singapore 7845 STREET",
            "company_registration_number": "SAMPLE78545REG",
            "company_country": "Singapore",
            "contact_email_id": "app@app.com",
            "website_contact_page_url": "http://appsample.com",
            "last_update_date": "2022-10-09"
            }




    def test_get_legalpolicies(self):
        res = self.client.get(f"{self.base_url}legalpolicies/")
        self.assertEqual(res.status_code, 200)


    def test_add_new_app_record(self):
        res = self.client.post(f"{self.base_url}legalpolicies/", json=self.new_app_data, headers= self.headers)
        self.assertEqual(res.status_code, 201)


