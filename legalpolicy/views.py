import os
import django
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from utils.dowell import (
    fetch_document,

    LEGAL_POLICY_COLLECTION,
    LEGAL_POLICY_DOCUMENT_NAME,
    LEGAL_POLICY_KEY
)
from dowelllegalpracticeapi.settings import BASE_DIR
from string import Template
from legalpolicy.serializers import (LegalPolicySerializer)



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


def load_public_legal_policy(request, app_event_id:str, policy:str):
    try:

        format = request.GET.get("format", "html")

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
        content = content.substitute(**data['policies_api'])
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

