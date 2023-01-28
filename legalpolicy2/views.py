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
from django.views.decorators.clickjacking import xframe_options_exempt

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
    ]



class IAgreeToPolicyStatus(APIView):

    def get(self, request, session_id, format= None):
        try:
            response_data = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            legal_policies = []

            query_data = IAgreeToPolicyTracker.objects.filter(session_id = session_id)
            for data in query_data:

                legal_policies.append(data.format())

            response_data= {
                "data": legal_policies,
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




class IAgreeToPolicyTrackerDetail(APIView):

    def get(self, request, session_id, format= None):
        try:
            response_data = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            query_data = IAgreeToPolicyTracker.objects.filter(policy_request_id = session_id).first()
            if query_data:
                response_data= {
                    "data": [query_data.format()],
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
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            response_data = {}

            query_data = IAgreeToPolicyTracker.objects.filter(policy_request_id = policy_request_id).first()
            print(query_data)
            if query_data:

                #update the tracker
                query_data.i_agree = request.data["i_agree"]
                query_data.i_agreed_datetime = datetime.now()
                query_data.save()
                
                response_data= {
                    "event_id": policy_request_id,
                    "session_id": query_data.session_id,
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




@xframe_options_exempt
def load_public_legal_policy(request, app_event_id:str, policy:str):
    try:

        format = request.GET.get("format", "html")
        redirect_url = request.GET.get("redirect_url", "none")
        session_id = request.GET.get("session_id", "")
        policy_request_id = f"{session_id}{policy}".upper()
        agreed_already_message = ""
        i_agree_status = 0

        try:

            # log request id 
            query_data = IAgreeToPolicyTracker.objects.filter(policy_request_id = policy_request_id).first()
            if not query_data:
                new_track = IAgreeToPolicyTracker()
                new_track.policy_request_id = policy_request_id
                new_track.legal_policy_type = policy
                new_track.session_id = session_id
                new_track.i_agree = False
                new_track.log_datetime = datetime.now()
                new_track.save()

            if query_data:
                # format message
                if query_data.i_agree:

                    mm = query_data.i_agreed_datetime.month
                    dd = query_data.i_agreed_datetime.day if query_data.i_agreed_datetime.day > 9 else f"0{query_data.i_agreed_datetime.day}"
                    yyyy = query_data.i_agreed_datetime.year

                    i_agree_status = 1
                    legal_policy_type = query_data.legal_policy_type.lower().replace("-", " ")
                    agreed_already_message = f"You agreed to these {legal_policy_type} on {MONTHS[mm-1]} {dd}, {yyyy}"


                
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
            policy_request_id = policy_request_id,
            agreed_already_message = agreed_already_message,
            i_agree_status = i_agree_status
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


