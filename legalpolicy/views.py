import os
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import jwt
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django.conf import settings
from datetime import datetime

from utils.dowell import (
    fetch_document,

    LEGAL_POLICY_COLLECTION,
    PRIVACY_CONSENT_COLLECTION,
    LEGAL_POLICY_DOCUMENT_NAME,
    PRIVACY_CONSENT_DOCUMENT_NAME,
    LEGAL_POLICY_KEY,
    PRIVACY_CONSENT_KEY,
    BASE_URL
)
from dowelllegalpracticeapi.settings import BASE_DIR
from string import Template
from legalpolicy.serializers import (LegalPolicySerializer, PrivacyConsentSerializer)



def index(request):
    return JsonResponse({
        "message": "Welcome to legal policy API"
    })


class LegalPolicyList(APIView):

    def get(self, request, format= None):
        try:
            response_data = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            limit = int(request.GET.get("limit", "10"))
            offset = int(request.GET.get("offset", "0"))

            action_type = request.GET.get("action_type", "0")
            search_term = request.GET.get("search_term", "")

            if action_type == "search":
                response_data = fetch_document(
                    LEGAL_POLICY_COLLECTION,
                    LEGAL_POLICY_DOCUMENT_NAME,
                    fields={
                        "policies_api.app_or_website_or_service_name": {
                            "$regex": f"{search_term}",
                            "$options": "i"
                            }
                        }
                    )

            else:
                response_data = fetch_document(
                    LEGAL_POLICY_COLLECTION,
                    LEGAL_POLICY_DOCUMENT_NAME,
                    fields={}
                    )

            status_code = status.HTTP_200_OK
            


        except Exception as err:
            print(str(err))
            return Response({
                "isSuccess": False,
                "error": status_code,
                "message": "Internal Server Error"
            }, status=status_code)

        else:
            return Response(response_data, status= status_code)

    def post(self, request, format= None):
        try:
            response_data = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            # create serializer object
            serializer= LegalPolicySerializer(data= request.data)

            if serializer.is_valid():
                response_data, status_code = serializer.save()
            else:
                print(str(serializer.errors))
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return Response({
                    "isSuccess": False,
                    "error": status_code,
                    "message": "Unprocessable"
                }, status=status_code)

        except Exception as err:
            print(str(err))
            return Response({
                "isSuccess": False,
                "error": status_code,
                "message": "Internal Server Error"
            }, status=status_code)

        else:
            return Response(response_data, status= status_code)


class LegalPolicyDetail(APIView):

    def get(self, request, event_id, format= None):
        try:
            response_data = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            response_data = fetch_document(
                LEGAL_POLICY_COLLECTION,
                LEGAL_POLICY_DOCUMENT_NAME,
                fields={"eventId": event_id}
                )
            status_code = status.HTTP_200_OK
            


        except Exception as err:
            print(str(err))
            return Response({
                "isSuccess": False,
                "error": status_code,
                "message": "Internal Server Error"
            }, status=status_code)

        else:
            return Response(response_data, status= status_code)


    def put(self, request, event_id, format= None):
        try:
            response_data = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            # create serializer object
            serializer= LegalPolicySerializer(event_id, data= request.data)

            if serializer.is_valid():
                response_data, status_code = serializer.update(event_id, serializer.validated_data)
            else:
                print(str(serializer.errors))
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return Response({
                    "isSuccess": False,
                    "error": status_code,
                    "message": "Unprocessable"
                }, status=status_code)

        except Exception as err:
            print(str(err))
            return Response({
                "isSuccess": False,
                "error": status_code,
                "message": "Internal Server Error"
            }, status=status_code)

        else:
            return Response(response_data, status= status_code)



def read_template(filename:str) -> Template:
    content=""

    # Get obsolute path
    file_path = os.path.join(BASE_DIR, f"templates/{filename}")

    # load content
    with open(file_path, 'r') as template_file:
        content = template_file.read()
        
    return Template(content)


def get_policy_template_name(policy:str) -> str:

    if policy == "app-privacy-policy":
        return "app-privacy-policy.html"

    elif policy == "mobile-app-privacy-policy-summary":
        return "mobile-app-privacy-policy-summary.html"

    elif policy == "disclaimer":
        return "disclaimer.html"
    
    elif policy == "website-privacy-policy":
        return "website-privacy-policy.html"

    elif policy == "cookies-policy":
        return "cookies-policy.html"

    elif policy == "terms-and-conditions":
        return "terms-and-conditions.html"

    elif policy == "end-user-license-agreement":
        return "end-user-license-agreement.html"

    elif policy == "return-refund-policy":
        return "return-refund-policy.html"

    elif policy == "safety-disclaimer":
        return "safety-disclaimer.html"

    elif policy == "security-policy-for-wifi-qr-code":
        return "security-policy-for-wifi-qr-code.html"

    elif policy == "website-security-policy":
        return "website-security-policy.html"



@xframe_options_exempt
def load_public_legal_policy(request, app_event_id:str, policy:str):
    try:

        format = request.GET.get("format", "html")
        redirect_url = request.GET.get("redirect_url", "/")
        from .rc_jwt import encode

        jwt_raw_data = {
            "app_event_id": app_event_id,
            "isSuccess": True,
        }


        jwt_token = encode(jwt_raw_data)
        redirect_url = f"{redirect_url}?token={jwt_token}"
        # print("redirect_url: ",redirect_url)


        # retrieve policy related data from
        # database
        response_data = fetch_document(
            LEGAL_POLICY_COLLECTION,
            LEGAL_POLICY_DOCUMENT_NAME,
            fields={"eventId": app_event_id}
            )
        
        data = response_data['data'][0]

        # load policy template from the filesystem
        content = read_template(get_policy_template_name(policy))

        # replace placeholders in the template with actual values
        content = content.substitute(
            **data['policies_api'],
            redirect_url=redirect_url,
            policy_request_id = ""
            )
        # return html context

        if format == "html":
            return HttpResponse(content= content)


        # return json data
        from django.http import JsonResponse
        return JsonResponse({
            "app_event_id": app_event_id,
            "content": content,
            "policy_type": policy
        })


    except Exception as err:
        print(str(err))
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PrivacyConsentList(APIView):

    def get(self, request, format=None):
        try:

            limit = int(request.GET.get("limit", "10"))
            offset = int(request.GET.get("offset", "0"))

            # Retrieve records
            response_json = fetch_document(
                collection=PRIVACY_CONSENT_COLLECTION,
                document=PRIVACY_CONSENT_DOCUMENT_NAME,
                fields={}
            )

            response_json = PrivacyConsentList.add_document_url(request, response_json)
            return Response(response_json,
                            status=status.HTTP_200_OK
                            )

        # The code below will
        # execute when error occur
        except Exception as e:
            print(f"{e}")
            return Response({
                "error_msg": f"{e}"
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def post(self, request: Request, format=None):
        try:
            request_data = request.data
            response_json = {}
            status_code = 500


            if request_data['platform_type'] == "Privacy-Consent":
                response_json, status_code = self.create_privacy_consent(
                    request_data,
                    response_json,
                    status_code)


            response_json = PrivacyConsentList.add_document_url(request, response_json)
            return Response(response_json, status=status_code)

        # The code below will
        # execute when error occur
        except Exception as e:
            print(f"{e}")
            response_json = {
                "isSuccess": False,
                "message": str(e),
                "error": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response_json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @staticmethod
    def add_document_url(request, response_data):
        data_list = response_data['data']
        new_data_list = []


        for data in data_list:
            privacy_consent = data[PRIVACY_CONSENT_DOCUMENT_NAME]

            privacy_consent['privacy_consent_url'] = request.build_absolute_uri(
                reverse('load_privacy_consent', kwargs={'event_id': data["eventId"]}))


            # add privacy consent to new data list
            data[PRIVACY_CONSENT_DOCUMENT_NAME] = privacy_consent
            new_data_list.append(data)

        if new_data_list:
            response_data['data'] = new_data_list

        return response_data


    def create_privacy_consent(self, request_data, response_json, status_code):

        # Create serializer object
        serializer = PrivacyConsentSerializer(data=request_data)

        # Commit data to database
        if serializer.is_valid():
            response_json, status_code = serializer.save()
        else:
            print(serializer.errors)
            response_json = {
                "isSuccess": False,
                "message": [{key:value} for key, value in serializer.errors.items()],
                "error": status.HTTP_500_INTERNAL_SERVER_ERROR
            }



            return Response(response_json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return result
        return response_json, status_code



class PrivacyConsentDetail(APIView):

    def get(self, request, event_id, format=None):
        try:

            # Retrieve record
            response_json = fetch_document(
                collection=PRIVACY_CONSENT_COLLECTION,
                document=PRIVACY_CONSENT_DOCUMENT_NAME,
                fields={"eventId": event_id}
            )

            response_json = PrivacyConsentList.add_document_url(request, response_json)
            return Response(response_json, status=status.HTTP_200_OK)

        # The code below will
        # execute when error occur
        except Exception as e:
            print(f"{e}")
            return Response({
                "error_msg": f"{e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, event_id, format=None):
        try:
            from datetime import date
            request_data = request.data
            response_json = {}
            status_code = 500

            # Retrieve old data
            old_response_data = fetch_document(
                collection=PRIVACY_CONSENT_COLLECTION,
                document=PRIVACY_CONSENT_DOCUMENT_NAME,
                fields={"eventId": event_id}
            )

            action_type = ""
            if "action_type" in request_data:
                action_type = request_data['action_type']


            if action_type == "submit-signature":
                response_json, status_code = self.submit_signature(
                    old_privacy_consent_data= old_response_data,
                    request_data= request_data,
                    response_json= response_json,
                    status_code= status_code)


            else:
                response_json, status_code = self.update_privacy_consent(
                    old_privacy_consent_data= old_response_data,
                    request_data= request_data,
                    response_json= response_json,
                    status_code= status_code)



            response_json = PrivacyConsentList.add_document_url(request, response_json)
            return Response(response_json, status=status_code)


        # The code below will
        # execute when error occur
        except Exception as e:
            print(f"{e}")
            response_json = {
                "isSuccess": False,
                "message": str(e),
                "error": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response_json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def submit_signature(self, old_privacy_consent_data, request_data, response_json, status_code):

        print(request_data)
        print(" ")
        print(" ")
        print(" ")
        print(" ")

        old_data = old_privacy_consent_data['data']
        new_privacy_consent = old_data[0][PRIVACY_CONSENT_DOCUMENT_NAME]

        new_privacy_consent['consent_status_detail'] = {
                "status": request_data['consent_status'],
                "datetime": datetime.utcnow().isoformat()
                }
        new_privacy_consent['individual_providing_consent_detail'] = {
                "name": request_data['name'],
                "address": request_data['address'],
                "signature": request_data['signature'],
                "datetime": datetime.utcnow().isoformat()
                }
        new_privacy_consent['is_locked'] = True

        # Update consent to personal data usage
        count = 0
        for usage in new_privacy_consent['consent_to_personal_data_usage']:

            if usage['description'] in request_data['personal_data_usage']:
                # Update status
                new_privacy_consent['consent_to_personal_data_usage'][count]['status'] = True
            else:
                new_privacy_consent['consent_to_personal_data_usage'][count]['status'] = False

            count += 1
        


        # Update and Commit data into database
        serializer = PrivacyConsentSerializer(
            old_privacy_consent_data, data=new_privacy_consent)

        if serializer.is_valid():
            response_json, status_code = serializer.update(
                old_privacy_consent_data, serializer.validated_data)

        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_json = {
                "isSuccess": False,
                "message": [str(error) for error in serializer.errors],
                "error": status_code
            }


        # return result
        return response_json, status_code


    def update_privacy_consent(self, old_privacy_consent_data, request_data, response_json, status_code):

        # Update and Commit data into database
        serializer = PrivacyConsentSerializer(
            old_privacy_consent_data, data=request_data)

        if serializer.is_valid():
            response_json, status_code = serializer.update(
                old_privacy_consent_data, serializer.validated_data)

        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_json = {
                "isSuccess": False,
                "message": [str(error) for error in serializer.errors],
                "error": status_code
            }


        # return result
        return response_json, status_code


def format_content(data):

    ### BENGIN  Statement Of Work
    # privacy_policy_personal_data_collected list
    if "privacy_policy_personal_data_collected" in data:
        content = ""
        for personal_data in data['privacy_policy_personal_data_collected']:
            content += f'{personal_data},'
        
        data['privacy_policy_personal_data_collected'] = content

    # deliverables expected in this scope of work list
    if "consent_to_personal_data_usage" in data:
        content = ""
        for usage in data['consent_to_personal_data_usage']:
            if usage['status']:
                content += f'<p><span>&nbsp;<input type="checkbox" checked class="consent-to-personal-data-usage" data-description="{usage["description"]}"> {usage["description"]}</span></p>'
            else:
                content += f'<p><span>&nbsp;<input type="checkbox" class="consent-to-personal-data-usage" data-description="{usage["description"]}"> {usage["description"]}</span></p>'
        
        data['consent_to_personal_data_usage'] = content

    ### END Statement Of Work


    return data




@xframe_options_exempt
def load_privacy_consent(request, event_id:str):
    try:

        # retrieve compliance related data from
        # database
        response_data = fetch_document(
            PRIVACY_CONSENT_COLLECTION,
            PRIVACY_CONSENT_DOCUMENT_NAME,
            fields={"eventId": event_id}
            )
        
        data = response_data['data'][0]
        privacy_consent = data[PRIVACY_CONSENT_DOCUMENT_NAME]

        # load template from the filesystem
        content = read_template("privacy -consent-form.html")

        # replace placeholders in the template with actual values
        privacy_consent = format_content(privacy_consent)

        base_url = "http://127.0.0.1:8000" if settings.DEBUG else  BASE_URL
        individual_providing_consent_detail = privacy_consent['individual_providing_consent_detail']
        consent_status_detail = privacy_consent['consent_status_detail']


        if "is_locked" not in privacy_consent:
            privacy_consent['is_locked'] = False
        if "company_website_url" not in privacy_consent:
            privacy_consent['company_website_url'] = ""


        content = content.substitute(
            event_id= event_id,
            **privacy_consent,
            base_url=base_url,
            **individual_providing_consent_detail,
            consent_confirm= consent_status_detail['status'],
            consent_datetime= consent_status_detail['datetime']
            )


        return HttpResponse(content= content)



    except Exception as err:
        print(str(err))
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)






