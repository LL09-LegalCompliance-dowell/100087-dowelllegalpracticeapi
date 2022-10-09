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


        self.update_app_data = {
            "platform_type": "App",
            "app_or_website_or_service_name": "Sample 2",
            "app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies",
            "description": "App Update",
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


    def test_get_detail_for_legalpolicy(self):
        res = self.client.get(f"{self.base_url}legalpolicies/FB1010000000166530784452123773/")
        self.assertEqual(res.status_code, 200)



    def test_search_detail_for_legalpolicy_using_app_or_website_name(self):
        res = self.client.get(
            f"{self.base_url}legalpolicies/?action_type=search&search_term=Sample")

        self.assertEqual(res.status_code, 200)


    def test_update_app_or_website_record(self):
        res = self.client.put(
            f"{self.base_url}legalpolicies/FB1010000000166530784452123773/",
            json=self.update_app_data, headers= self.headers)

        self.assertEqual(res.status_code, 200)





