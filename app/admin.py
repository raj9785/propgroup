from django.contrib import admin
from .models import State,City,Zone,ZoneBoundry,Location,LocationBoundry,UserProfile

def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username','get_email','mobile','user_type','is_active')
    list_per_page = 20  # record 10 per page
    list_filter = ("is_active",)
    #inlines = [LeaveRecordAdmin, ]
    search_fields = ['user__first_name', 'user__last_name','user__email','mobile']

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     is_active__exact = request.GET.get('is_active__exact', '1')  # Default value is '2'
    #     qs = qs.filter(is_active=is_active__exact)
    #     return qs


    def get_username(self, obj):
        if obj.user.first_name or obj.user.last_name:
          return f"{obj.user.first_name} {obj.user.last_name}"
        else:
          return  "-----"   
    get_username.short_description = 'Name'


    

    def get_email(self, obj):
        if obj.user.email:
           return f"{obj.user.email}"
        else:
          return  "-----"   
    get_email.short_description = 'Email'
    
    def has_delete_permission(self, request, obj=None):
        return False  
    

admin.site.register(UserProfile, UserProfileAdmin)


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


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name','zone',"city",'state','is_active')
    list_per_page = 25
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(Location, LocationAdmin)



class LocationBoundryAdmin(admin.ModelAdmin):
    change_form_template = 'admin/app/location_boundry/change_form.html'
    add_form_template = 'admin/app/location_boundry/add_form.html'
    list_display = ('location',"latitude",'longitude','sequence_number')
    list_per_page = 25
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(LocationBoundry, LocationBoundryAdmin)

