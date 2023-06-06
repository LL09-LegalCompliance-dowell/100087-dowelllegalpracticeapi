from django.urls import path
from .views import (
    LegalPolicyList,
    LegalPolicyDetail,
    PrivacyConsentList,
    PrivacyConsentDetail,
    PrivacyConsentStatus
)


urlpatterns = [
    path("legalpolicies/", LegalPolicyList.as_view(), name="legalpolicies"),
    path("legalpolicies/<str:event_id>/", LegalPolicyDetail.as_view(), name="legalpolicydetail"),
    path("privacyconsents/", PrivacyConsentList.as_view(), name="legalpolicies"),
    path("privacyconsents/<str:event_id>/", PrivacyConsentDetail.as_view(), name="legalpolicydetail"),
    path('privacyconsents/<str:app_event_id>/<str:session_id>/status/', PrivacyConsentStatus.as_view(), name= "privacy_consent_status"),
]