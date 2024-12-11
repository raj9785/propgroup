from django.contrib import admin
from .models import Landmark

def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class LandmarkAdmin(admin.ModelAdmin):
    list_display = ('name','description',"city",'state','zone','is_active')
    list_per_page = 25
   
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

#admin.site.register(Landmark, LandmarkAdmin)