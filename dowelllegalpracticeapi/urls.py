"""dowelllegalpracticeapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from legalpolicy import views as vlp
from legalpolicy2 import views as vlp2
from django.conf.urls.static import static
from django.conf import settings
from legalpolicy.views import load_privacy_consent




urlpatterns = [

    path('admin/', admin.site.urls),
    path("api/", include("legalpolicy.urls")),
    path("api/", include("legalpolicy2.urls")),
    path("policy/<str:app_event_id>/<str:policy>/", vlp.load_public_legal_policy, name="load_public_legal_policy"),
    path("legalpolicies/<str:app_event_id>/<str:policy>/policies/", vlp2.load_public_legal_policy, name="tkr_load_public_legal_policy"),
    path("legalpolicies/testguides/", include("legalpolicyapi_testguide.urls")),
    path('privacyconsents/<str:app_event_id>/', load_privacy_consent, name= "load_privacy_consent"),
    path('', vlp.index, name="index")
]\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
