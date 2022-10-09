from ast import pattern
from django.urls import path
from .views import (
    LegalPolicyList,
    LegalPolicyDetail
)


urlpatterns = [
    path("legalpolicies/", LegalPolicyList.as_view(), name="legalpolicies"),
    path("legalpolicies/<str:event_id>/", LegalPolicyDetail.as_view(), name="legalpolicydetail")
]