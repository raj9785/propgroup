from django.db import models
from app.models import Zone,City,State

class Project(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, blank=False, related_name='project_state')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, blank=False, related_name='project_city')
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, null=True, blank=False, related_name='project_zone')
    project_name = models.CharField(max_length=255,null=True, blank=False)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to='icons/',
                             verbose_name="Icon", null=True, blank=False,max_length=255)
    image = models.FileField(upload_to='images/',
                             verbose_name="Image", null=True, blank=False,max_length=255)
    latitude = models.CharField(max_length=20, null=True, blank=False)
    longitude = models.CharField(max_length=20, null=True, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('state','city','zone','project_name')
        verbose_name = "Project"
        verbose_name_plural = "Project List"
    
    def __str__(self):
        return self.project_name