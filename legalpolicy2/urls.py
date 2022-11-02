from django.urls import path
from .views import IAgreeToPolicyTrackerDetail

urlpatterns = [
    path("tkr-legalpolicies/<str:policy_request_id>/", IAgreeToPolicyTrackerDetail.as_view(), name="tkr_legalpolicydetail")
]