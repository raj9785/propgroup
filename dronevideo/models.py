from django.db import models
from app.models import Zone,City,State

class DroneVideo(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, blank=False, related_name='drone_video_state')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, blank=False, related_name='drone_video_city')
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, null=True, blank=False, related_name='drone_video_zone')
    video_url = models.URLField(max_length=255, null=True, blank=False)
    title = models.CharField(max_length=255,null=True, blank=False)
    description = models.TextField(blank=True, null=True)
    path_color_code = models.CharField(max_length=7, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('state','city','zone','video_url')
        verbose_name = "Drone Video"
        verbose_name_plural = "Drone Video List"
    
    def __str__(self):
        return self.title +" [" +self.video_url+"]"
    

class DroneVideoPath(models.Model):
    drone_video = models.ForeignKey(
        DroneVideo, on_delete=models.CASCADE, null=True, blank=False, related_name='drone_video_path')
    latitude = models.CharField(max_length=20, null=True, blank=False)
    longitude = models.CharField(max_length=20, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    class Meta:
        verbose_name = "Drone Video Path"
        verbose_name_plural = "Drone Video Path List"
        unique_together = ('drone_video','latitude','longitude')

    def __str__(self):
        return str(self.latitude)+","+ str(self.longitude)
