from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from utils.dowell import (
    fetch_document,

    LEGAL_POLICY_COLLECTION,
    LEGAL_POLICY_DOCUMENT_NAME,
    LEGAL_POLICY_KEY
)

from legalpolicy.serializers import (LegalPolicySerializer)


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