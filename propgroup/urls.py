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

admin.site.site_header = 'Prop360d'
admin.site.site_title = "Prop360d Admin Portal"
admin.site.index_title = "Welcome to Prop360d Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('zone_list', views.zone_list,name="zone_list"),
    path('saveroute', views.saveroute,name="saveroute"),
    path('location_list', views.location_list,name="location_list"),
    path('get_video_list', views.get_video_list,name="get_video_list"),
    path('savelocationboundry', views.savelocationboundry,name="savelocationboundry"),
    path('save_drone_path_video', views.save_drone_path_video,name="save_drone_path_video"),
    path('ajax_login', views.ajax_login, name="ajax_login"),
    path('ajax_verify_otp', views.ajax_verify_otp, name="ajax_verify_otp"),
    path('ajax_send_otp', views.ajax_send_otp, name="ajax_send_otp"),
    path('ajax_register', views.ajax_register, name="ajax_register"),
    path('ajax_polygons', views.ajax_polygons, name="ajax_polygons"),
    path('ajax_location_polygons', views.ajax_location_polygons, name="ajax_location_polygons"),
    path('ajax_get_markers', views.ajax_get_markers, name="ajax_get_markers"),
    path('ajax_drone_video_paths', views.ajax_drone_video_paths, name="ajax_drone_video_paths"),
    path('ajax_get_video_list', views.ajax_get_video_list, name="ajax_get_video_list"),
    path('get_map_form', views.get_map_form, name="get_map_form"),
    path('save_map', views.save_map, name="save_map"),
    path('find_zone', views.find_zone, name="find_zone"),
    path('logout', views.logout_view, name = 'logout'), 
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)