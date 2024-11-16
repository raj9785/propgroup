from django.contrib import admin

from .models import Project

def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name','description',"city",'state','zone','is_active')
    list_per_page = 25
    
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(Project, ProjectAdmin)