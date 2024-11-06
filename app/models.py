from django.db import models

class State(models.Model):
    state_name = models.CharField(max_length=50, null=True, blank=False)
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

    def __str__(self):
        return self.city_name