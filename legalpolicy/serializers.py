from email.policy import default
from platform import platform
from rest_framework import serializers, status
from utils.dowell import (
    save_document,
    update_document,
    fetch_document,

    LEGAL_POLICY_COLLECTION,
    LEGAL_POLICY_DOCUMENT_NAME,
    LEGAL_POLICY_KEY
)

PLATFORM_TYPE = (("App", "App"), ("Website", "Website"), ("Template", "Template"))


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

