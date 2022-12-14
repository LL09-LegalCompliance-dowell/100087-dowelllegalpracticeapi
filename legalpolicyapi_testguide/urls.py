from django.urls import path
from .views import index

app_name = "legalpolicyapi_testguide"
urlpatterns = [
    path("", index, name="index")
]