"""
URL configuration for propgroup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from app import views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

admin.site.site_header = 'Property Group'
admin.site.site_title = "Property Group Admin Portal"
admin.site.index_title = "Welcome to Property Group Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('leafletjs', views.leafletjs, name="leafletjs"),
    path('zone_list', views.zone_list,name="zone_list"),
    path('saveroute', views.saveroute,name="saveroute"),
    path('location_list', views.location_list,name="location_list"),
    path('savelocationboundry', views.savelocationboundry,name="savelocationboundry"),
]
