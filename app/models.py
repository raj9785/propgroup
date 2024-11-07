from django.db import models

class State(models.Model):
    state_name = models.CharField(max_length=50,unique=True, null=True, blank=False)
    state_code = models.CharField(max_length=5, null=True, blank=True)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"

    def __str__(self):
        return self.state_name


class City(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, blank=False, related_name='state_list')
    city_name = models.CharField(max_length=50, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = ('state','city_name')

    def __str__(self):
        return self.city_name
    

class Zone(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, blank=False, related_name='zone_state_list')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, blank=False, related_name='zone_city_list')
    zone_name = models.CharField(max_length=50, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"
        unique_together = ('state','city','zone_name')

    def __str__(self):
        return self.zone_name
    
class ZoneBoundry(models.Model):
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, null=True, blank=False, related_name='zones')
    latitude = models.CharField(max_length=20, null=True, blank=False)
    longitude = models.CharField(max_length=20, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    class Meta:
        verbose_name = "Zone Boundry"
        verbose_name_plural = "Zone Boundries"
        unique_together = ('zone','latitude','longitude')


class Location(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, blank=False, related_name='location_state_list')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, blank=False, related_name='location_city_list')
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, null=True, blank=False, related_name='location_zone_list')
    location_name = models.CharField(max_length=50, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        unique_together = ('state','city','zone','location_name')

    def __str__(self):
        return self.location_name
        

class LocationBoundry(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True, blank=False, related_name='locations')
    latitude = models.CharField(max_length=20, null=True, blank=False)
    longitude = models.CharField(max_length=20, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    class Meta:
        verbose_name = "Location Boundry"
        verbose_name_plural = "Location Boundries"
        unique_together = ('location','latitude','longitude')
