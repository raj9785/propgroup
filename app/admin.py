from django.contrib import admin
from .models import State,City,Zone,ZoneBoundry

def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class StateAdmin(admin.ModelAdmin):
    list_display = ('state_name','state_code','is_active')
    list_per_page = 25
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(State, StateAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name','state','is_active')
    list_per_page = 25
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(City, CityAdmin)



class ZoneAdmin(admin.ModelAdmin):
    list_display = ('zone_name',"city",'state','is_active')
    list_per_page = 25
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(Zone, ZoneAdmin)



class ZoneBoundryAdmin(admin.ModelAdmin):
    change_form_template = 'admin/app/zone_boundry/change_form.html'
    add_form_template = 'admin/app/zone_boundry/add_form.html'
    list_display = ('zone',"latitude",'longitude','sequence_number')
    list_per_page = 25
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(ZoneBoundry, ZoneBoundryAdmin)