from email.policy import default
from platform import platform
from rest_framework import serializers, status
from datetime import datetime
from utils.dowell import (
    save_document,
    update_document,
    fetch_document,

    LEGAL_POLICY_COLLECTION,
    PRIVACY_CONSENT_COLLECTION,
    LEGAL_POLICY_DOCUMENT_NAME,
    PRIVACY_CONSENT_DOCUMENT_NAME,
    LEGAL_POLICY_KEY,
    PRIVACY_CONSENT_KEY
)

PLATFORM_TYPE = (("App", "App"), ("Website", "Website"), ("Template", "Template"), ("Privacy-Consent", "Privacy-Consent"))


class LegalPolicySerializer(serializers.Serializer):
    """
     Retrieve, update and  create Dowell legal policy
    """

    platform_type = serializers.ChoiceField(choices=PLATFORM_TYPE, default="App")
    app_or_website_or_service_name = serializers.CharField(max_length=100, allow_blank=False, required=True)
    app_or_website_or_service_url = serializers.URLField(required=True)
    description = serializers.CharField(max_length=500, allow_blank=True, required=False, default= " ")
    company_name = serializers.CharField(max_length=100, allow_blank=False, required=True)
    company_address = serializers.CharField(max_length=500, allow_blank=False, required=True)
    company_registration_number = serializers.CharField(max_length=50, allow_blank=False, required=True)
    company_country = serializers.CharField(max_length=50, allow_blank=False, required=True)
    contact_email_id = serializers.EmailField(required=True)
    website_contact_page_url = serializers.URLField(required=True)
    last_update_date = serializers.CharField(max_length=50, allow_blank=False, required=True)
    app_or_website_governed_by_or_jurisdiction = serializers.CharField(max_length=100, allow_blank=True, required=False, default= " ")
    days_allowed_for_cancellation_of_order_or_product = serializers.IntegerField(required=False, default= 0)
    reimburse_days = serializers.IntegerField(required=False, default= 0)


    def create(self, validated_data):
        response_data = {}
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        # Add app/website detail to database
        response_data = save_document(
            collection=LEGAL_POLICY_COLLECTION,
            document=LEGAL_POLICY_DOCUMENT_NAME,
            key=LEGAL_POLICY_KEY,
            value=validated_data
        )

        # Retrieve app/website detail from database         
        if response_data["isSuccess"]:
            status_code = status.HTTP_201_CREATED

            # Retrieve data
            response_data = fetch_document(
                collection=LEGAL_POLICY_COLLECTION,
                document=LEGAL_POLICY_DOCUMENT_NAME,
                fields={
                    "eventId": response_data["event_id"]
                }
            )

        return response_data, status_code

    def update(self, event_id, validated_data):

        response_data = {}
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        # update app/website detail to database
        response_data = update_document(
            collection=LEGAL_POLICY_COLLECTION,
            document=LEGAL_POLICY_DOCUMENT_NAME,
            key=LEGAL_POLICY_KEY,
            new_value=validated_data,
            event_id=event_id
        )

        # Retrieve app/website detail from database
        if response_data["isSuccess"]:
            status_code = status.HTTP_200_OK

            # Retrieve data
            response_data = fetch_document(
                collection=LEGAL_POLICY_COLLECTION,
                document=LEGAL_POLICY_DOCUMENT_NAME,
                fields={"eventId": event_id}
            )

        return response_data, status_code


class PrivacyConsentSerializer(serializers.Serializer):
    """
     Retrieve, update and  create privacy consent


    """

    platform_type = serializers.ChoiceField(choices=PLATFORM_TYPE, default="Privacy-Consent")
    consent_status_detail = serializers.DictField(default={})
    individual_providing_consent_detail = serializers.DictField(default={})
    company_name = serializers.CharField(max_length=100, allow_blank=False, required=True)
    company_email = serializers.EmailField(required=True)
    privacy_policy_personal_data_collected = serializers.ListField(default=[])
    consent_to_personal_data_usage = serializers.ListField(default={}) # will be checkout by the receipient
    company_website_url = serializers.URLField(required=True)
    privacy_policy_url = serializers.URLField(required=True)


    def create(self, validated_data):
        response_data = {}
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        validated_data['created_datetime'] = datetime.utcnow().isoformat()
        validated_data['last_updated_datetime'] = datetime.utcnow().isoformat()

        # Add app/website detail to database
        response_data = save_document(
            collection=PRIVACY_CONSENT_COLLECTION,
            document=PRIVACY_CONSENT_DOCUMENT_NAME,
            key=PRIVACY_CONSENT_KEY,
            value=validated_data
        )

        # Retrieve app/website detail from database         
        if response_data["isSuccess"]:
            status_code = status.HTTP_201_CREATED

            # Retrieve data
            response_data = fetch_document(
                collection=PRIVACY_CONSENT_COLLECTION,
                document=PRIVACY_CONSENT_DOCUMENT_NAME,
                fields={
                    "eventId": response_data["event_id"]
                }
            )

        print(response_data)
        return response_data, status_code


    def update(self, event_id, validated_data):

        response_data = {}
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        validated_data['last_updated_datetime'] = datetime.utcnow().isoformat()


        # Retrieve old data
        old_response_data = fetch_document(
            collection=PRIVACY_CONSENT_COLLECTION,
            document=PRIVACY_CONSENT_DOCUMENT_NAME,
            fields={"eventId": event_id}
        )

        old_data = old_response_data['data']
        print(old_data)
        old_privacy_consent = old_data[0][PRIVACY_CONSENT_DOCUMENT_NAME]

        new_value={**old_privacy_consent, **validated_data}

        # update app/website detail to database
        response_data = update_document(
            collection=PRIVACY_CONSENT_COLLECTION,
            document=PRIVACY_CONSENT_DOCUMENT_NAME,
            key=PRIVACY_CONSENT_KEY,
            new_value=new_value,
            event_id=event_id
        )

        # Retrieve app/website detail from database
        if response_data["isSuccess"]:
            status_code = status.HTTP_200_OK

            old_data[0][PRIVACY_CONSENT_DOCUMENT_NAME] = new_value
            old_response_data['data'] = old_data
            response_data = old_response_data

        return response_data, status_code
