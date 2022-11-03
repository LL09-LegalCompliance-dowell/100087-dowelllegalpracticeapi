import os
from rest_framework.response import Response
from utils.dowell import (
    fetch_document,

    LEGAL_POLICY_COLLECTION,
    LEGAL_POLICY_DOCUMENT_NAME,
    LEGAL_POLICY_KEY
)
from dowelllegalpracticeapi.settings import BASE_DIR
from django.http import HttpResponse
from legalpolicy.views import get_policy_template_name, read_template
from . models import IAgreeToPolicyTracker
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class IAgreeToPolicyTrackerDetail(APIView):

    def get(self, request, policy_request_id, format= None):
        try:
            response_data = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            query_data = IAgreeToPolicyTracker.objects.filter(policy_request_id = policy_request_id).first()
            if query_data:
                response_data= {
                    "policy_request_id": policy_request_id,
                    "i_agree": query_data.i_agree,
                    "isSuccess": True,
                }
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


    def put(self, request, policy_request_id, format= None):
        try:
            response_data = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            query_data = IAgreeToPolicyTracker.objects.filter(policy_request_id = policy_request_id).first()
            if query_data:

                print(request.data)
                #update the tracker
                query_data.i_agree = request.data["i_agree"]
                query_data.save()
                
                response_data= {
                    "policy_request_id": policy_request_id,
                    "isSuccess": True
                }

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





def load_public_legal_policy(request, app_event_id:str, policy:str):
    try:

        format = request.GET.get("format", "html")
        redirect_url = request.GET.get("redirect_url", "/")
        policy_request_id = request.GET.get("policy_request_id", "")

        try:
            # log request id 
            query_data = IAgreeToPolicyTracker.objects.filter(policy_request_id = policy_request_id).first()
            if query_data:
                query_data.i_agree = True
                query_data.save()

            else:
                new_track = IAgreeToPolicyTracker()
                new_track.policy_request_id = policy_request_id
                new_track.i_agree = False
                new_track.log_datetime = datetime.now()
                new_track.save()
                
        except Exception as err:
            print(str(err))

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
            redirect_url = redirect_url,
            policy_request_id = policy_request_id
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


