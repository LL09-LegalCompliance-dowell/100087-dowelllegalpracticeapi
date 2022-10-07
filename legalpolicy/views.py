from  rest_framework.views import APIView
from  rest_framework import status
from  rest_framework.response import Response


class LegalPolicyList(APIView):

    def get(self, request, format= None):
        return Response({
            "Message": "Initial Setup"
        })
