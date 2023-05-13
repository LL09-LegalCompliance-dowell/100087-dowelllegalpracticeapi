from django.urls import path
from .views import (
    LegalPolicyList,
    LegalPolicyDetail,
    PrivacyConsentList,
    PrivacyConsentDetail
)


urlpatterns = [
    path("legalpolicies/", LegalPolicyList.as_view(), name="legalpolicies"),
    path("legalpolicies/<str:event_id>/", LegalPolicyDetail.as_view(), name="legalpolicydetail"),
    path("privacyconsents/", PrivacyConsentList.as_view(), name="legalpolicies"),
    path("privacyconsents/<str:event_id>/", PrivacyConsentDetail.as_view(), name="legalpolicydetail")
] #load_privacy_consent