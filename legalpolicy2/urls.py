from django.urls import path
from .views import IAgreeToPolicyTrackerDetail, IAgreeToPolicyStatus

urlpatterns = [
    path("legalpolicies/<str:policy_request_id>/iagreelogs/", IAgreeToPolicyTrackerDetail.as_view(), name="tkr_legalpolicydetail"),
    path("legalpolicies/<str:session_id>/iagreestatus/", IAgreeToPolicyStatus.as_view(), name="agreetopolicystatus")
]