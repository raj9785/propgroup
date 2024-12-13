from django.contrib import admin
from .models import DroneVideo,DroneVideoPath

def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class DroneVideoPathAdmin(admin.StackedInline):
    model = DroneVideoPath
    extra = 1  

class DroneVideoAdmin(admin.ModelAdmin):
    list_display = ('user','video_url','title',"city",'state','zone','is_active')
    list_per_page = 25
    #inlines = [DroneVideoPathAdmin,]
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(DroneVideo, DroneVideoAdmin)


class DroneVideoAdminLeftPanel(admin.ModelAdmin):
    change_form_template = 'admin/dronevideo/drone_video_path/change_form.html'
    add_form_template = 'admin/dronevideo/drone_video_path/add_form.html'
    list_display = ('drone_video','get_title',"latitude",'longitude','sequence_number')
    list_per_page = 25
    def get_title(self, obj):
        return f"{obj.drone_video.title}"
    get_title.short_description = 'video title'
    get_title.admin_order_field = 'drone_video__title'
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

#admin.site.register(DroneVideoPath, DroneVideoAdminLeftPanel)
