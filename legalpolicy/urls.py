from ast import pattern
from django.urls import path
from .views import (
    LegalPolicyList
)


urlpatterns = [
    path("legalpolicies/", LegalPolicyList.as_view(), name="legalpolicies")
]