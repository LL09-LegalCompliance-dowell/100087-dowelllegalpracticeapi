# 100087-dowelllegalpracticeapi

## Dowell Legal Policy API Reference


### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:8000/`, which is set as a proxy in the frontend configuration.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "isSuccess": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable


### Endpoints

### Legal Policy

#### GET /api/legalpolicies/

- General:
  - Returns a list of legal policy objects such as (apps, website and service) details, and success value
- Sample: `curl http://127.0.0.1:8000/api/legalpolicies/` or open link in a browser

```

{
    "isSuccess": true,
    "data": [
        {
            "_id": "63428eb8317ec81d6c6c7ffd",
            "eventId": "FB1010000000001665306290565391",
            "policies_api": {
                "platform_type": "App",
                "app_or_website_or_service_name": "LegalZard",
                "app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies",
                "description": "App description",
                "company_name": "Dowell",
                "company_address": "Singapore 7845 STREET",
                "company_registration_number": "SAMPLE78545REG",
                "company_country": "Singapore",
                "contact_email_id": "app@app.com",
                "website_contact_page_url": "http://appsample.com",
                "last_update_date": "2022-10-09",
                "app_or_website_governed_by_or_jurisdiction": " ",
                "days_allowed_for_cancellation_of_order_or_product": 90,
                "reimburse_days": 30
            }
        },
        {
            "_id": "634294ca15c82260d06c7c3d",
            "eventId": "FB1010000000166530784452123773",
            "policies_api": {
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
                "last_update_date": "2022-10-09",
                "app_or_website_governed_by_or_jurisdiction": " ",
                "days_allowed_for_cancellation_of_order_or_product": 90,
                "reimburse_days": 30
            }
        }
    ]
}

```

#### POST /api/legalpolicies/

- General:
  - Creates a new app, website and services details using the submitted json data, Returns the detail, success value, and event id.
- `curl http://127.0.0.1:8000/api/legalpolicies -X POST -H "Content-Type: application/json" -d '{"platform_type": "App","app_or_website_or_service_name": "LegalZard","app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies","description": "App description",
"company_name": "Dowell","company_address": "Singapore 7845 STREET","company_registration_number": "SAMPLE78545REG","company_country": "Singapore","contact_email_id": "app@app.com","website_contact_page_url": "http://appsample.com","last_update_date": "2022-10-09", "app_or_website_governed_by_or_jurisdiction": " ","days_allowed_for_cancellation_of_order_or_product": 90,"reimburse_days": 30}'`

- You can also open the link `http://127.0.0.1:8000/api/licenses/` in a browser and perform the post operation

```
{
    "isSuccess": true,
    "data": [
        {
            "_id": "63428eb8317ec81d6c6c7ffd",
            "eventId": "FB1010000000001665306290565391",
            "policies_api": {
                "platform_type": "App",
                "app_or_website_or_service_name": "LegalZard",
                "app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies",
                "description": "App description",
                "company_name": "Dowell",
                "company_address": "Singapore 7845 STREET",
                "company_registration_number": "SAMPLE78545REG",
                "company_country": "Singapore",
                "contact_email_id": "app@app.com",
                "website_contact_page_url": "http://appsample.com",
                "last_update_date": "2022-10-09",
                "app_or_website_governed_by_or_jurisdiction": " ",
                "days_allowed_for_cancellation_of_order_or_product": 90,
                "reimburse_days": 30
            }
        }
        
    ]
}

```


#### GET /api/legalpolicies/{event_id}/

- General:
  - Returns a list of legal policy objects, and success value
- Sample: `curl http://127.0.0.1:8000/api/legalpolicies/FB1010000000001665306290565391/` or open link in a browser

```
{
    "isSuccess": true,
    "data": [
        {
            "_id": "63428eb8317ec81d6c6c7ffd",
            "eventId": "FB1010000000001665306290565391",
            "policies_api": {
                "platform_type": "App",
                "app_or_website_or_service_name": "LegalZard",
                "app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies",
                "description": "App description",
                "company_name": "Dowell",
                "company_address": "Singapore 7845 STREET",
                "company_registration_number": "SAMPLE78545REG",
                "company_country": "Singapore",
                "contact_email_id": "app@app.com",
                "website_contact_page_url": "http://appsample.com",
                "last_update_date": "2022-10-09",
                "app_or_website_governed_by_or_jurisdiction": " ",
                "days_allowed_for_cancellation_of_order_or_product": 90,
                "reimburse_days": 30
            }
        }
        
    ]
}

```

#### PUT /api/legalpolicies/{event_id}/

- General:
  - update legal policy object detail for app, website and services using the submitted json data, Returns the detail, success value, and event id.
- `curl http://127.0.0.1:8000/api/legalpolicies -X POST -H "Content-Type: application/json" -d '{"platform_type": "App","app_or_website_or_service_name": "LegalZard Part","app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies","description": "App description",
"company_name": "Dowell","company_address": "Singapore 7845 STREET","company_registration_number": "SAMPLE78545REG","company_country": "Singapore","contact_email_id": "app@app.com","website_contact_page_url": "http://appsample.com","last_update_date": "2022-10-09", "app_or_website_governed_by_or_jurisdiction": " ",                "days_allowed_for_cancellation_of_order_or_product": 90,"reimburse_days": 30}'`

- You can also open the link `http://127.0.0.1:8000/api/legalpolicies/FB1010000000001665306290565391/` in a browser and perform the post operation

```
{
    "isSuccess": true,
    "data": [
        {
            "_id": "63428eb8317ec81d6c6c7ffd",
            "eventId": "FB1010000000001665306290565391",
            "policies_api": {
                "platform_type": "App",
                "app_or_website_or_service_name": "LegalZard Part",
                "app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies",
                "description": "App description",
                "company_name": "Dowell",
                "company_address": "Singapore 7845 STREET",
                "company_registration_number": "SAMPLE78545REG",
                "company_country": "Singapore",
                "contact_email_id": "app@app.com",
                "website_contact_page_url": "http://appsample.com",
                "last_update_date": "2022-10-09",
                "app_or_website_governed_by_or_jurisdiction": " ",
                "days_allowed_for_cancellation_of_order_or_product": 90,
                "reimburse_days": 30
            }
        }
        
    ]
}

```


#### GET /api/legalpolicies/?search_term=LegalZard&action_type=search

- General:
  - Search the legal policy detail and Return query result.
- `curl http://127.0.0.1:8000/api/legalpolicies/?search_term=LegalZard&action_type=search -X GET`

```
{
    "isSuccess": true,
    "data": [
        {
            "_id": "63428eb8317ec81d6c6c7ffd",
            "eventId": "FB1010000000001665306290565391",
            "policies_api": {
                "platform_type": "App",
                "app_or_website_or_service_name": "LegalZard Part",
                "app_or_website_or_service_url": "https://play.google.com/store/apps/details?id=com.dowelllicenses.policies",
                "description": "App description",
                "company_name": "Dowell",
                "company_address": "Singapore 7845 STREET",
                "company_registration_number": "SAMPLE78545REG",
                "company_country": "Singapore",
                "contact_email_id": "app@app.com",
                "website_contact_page_url": "http://appsample.com",
                "last_update_date": "2022-10-09",
                "app_or_website_governed_by_or_jurisdiction": " ",
                "days_allowed_for_cancellation_of_order_or_product": 90,
                "reimburse_days": 30
            }
        }
        
    ]
}

```



### Legal Policy API (I agree checkbox selected response)


#### GET /legalpolicies/{app_event_id}/{policy_type}/policies/?redirect_url={callbackurl}&session_id={session_id}
 session_id=FB101000000000166530629056539143455595

- General:
  - This always load legal privacy policy.
  - `http://127.0.0.1:8000/legalpolicies/FB1010000000001665306290565391/app-privacy-policy/policies/?redirect_url=http://127.0.0.1:8000/callbackurl&session_id=FB101000000000166530629056539143455595`




#### GET /api/legalpolicies/{session_id}/iagreestatus/

- General:
  -  Call to this endpoint get "i agree" status on callback.
  - `http://127.0.0.1:8000/api/legalpolicies/FB101000000000166530629056539143455595/iagreestatus/`

```
{
    "data": [
        {
            "event_id": "FB101000000000166530629056539143455595APP-PRIVACY-POLICY",
            "session_id": "FB101000000000166530629056539143455595",
            "i_agree": true,
            "log_datetime": "2022-12-08T18:33:58.064201+00:00",
            "i_agreed_datetime": "2022-12-08T18:34:14.471947+00:00",
            "legal_policy_type": "app-privacy-policy"
        },
        {
            "event_id": "FB101000000000166530629056539143455595WEBSITE-PRIVACY-POLICY",
            "session_id": "FB101000000000166530629056539143455595",
            "i_agree": true,
            "log_datetime": "2022-12-08T18:41:47.335695+00:00",
            "i_agreed_datetime": "2022-12-08T18:42:06.403831+00:00",
            "legal_policy_type": "website-privacy-policy"
        }
    ],
    "isSuccess": true
}

```

#### PUT /api/legalpolicies/{event_id}/iagreelogs/

- General:
  -  Call this endpoint  update "i agree" status when click/selected, it is achive by javascript embedded legal policy web page.
  - `curl -i -X PUT -d '{"i_agree": true}' -H "Content-Type: application/json" http://127.0.0.1:8000/api/legalpolicies/FB101000000000166530629056539143455595WEBSITE-PRIVACY-POLICY/iagreelogs/`

```  
{
    "event_id": "FB101000000000166530629056539143455595WEBSITE-PRIVACY-POLICY",
    "session_id": "FB101000000000166530629056539143455595",
    "isSuccess": true
}

```



### Types of Policy
- [app-privacy-policy](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/app-privacy-policy/)
- [mobile-app-privacy-policy-summary](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/mobile-app-privacy-policy-summary/)
- [disclaimer](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/disclaimer/)
- [website-privacy-policy](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/website-privacy-policy/)
- [cookies-policy](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/cookies-policy/)
- [terms-and-conditions](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/terms-and-conditions/)
- [end-user-license-agreement](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/end-user-license-agreement/)
- [return-refund-policy](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/return-refund-policy/)
- [safety-disclaimer](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/safety-disclaimer/)
- [security-policy-for-wifi-qr-code](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/security-policy-for-wifi-qr-code/)
- [website-security-policy](https://100087.pythonanywhere.com/policy/FB1010000000001665306290565391/website-security-policy/)
