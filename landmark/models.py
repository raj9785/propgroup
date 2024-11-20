from django.db import models
from app.models import Zone,City,State

class Landmark(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, blank=False, related_name='landmark_state')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, blank=False, related_name='landmark_city')
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, null=True, blank=False, related_name='landmark_zone')
    name = models.CharField(max_length=40,null=True, blank=False,verbose_name="Title")
    description = models.TextField(blank=True, null=True,max_length=80)
    icon = models.FileField(upload_to='icons/',
                             verbose_name="Icon", null=True, blank=True,max_length=255)
    latitude = models.CharField(max_length=20, null=True, blank=False)
    longitude = models.CharField(max_length=20, null=True, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('state','city','zone','name')
        verbose_name = "Landmark"
        verbose_name_plural = "Landmark List"
    
    def __str__(self):
        return self.name
    