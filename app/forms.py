from django import forms

from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from landmark.models import Landmark
from .models import State,City,Location,Zone
from projects.models import Project
from dronevideo.models import DroneVideo


class LandmarkForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Name',max_length=50,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    description = forms.CharField(required=True, label='Description',max_length=80,widget=forms.TextInput(attrs={'class': 'form-control'}))
    state=forms.ModelChoiceField(required=False, 
        queryset=State.objects.filter(is_active=True),empty_label="Select State",widget=forms.Select(attrs={'class': 'form-control'})) 
    city=forms.ModelChoiceField(required=False, 
        queryset=City.objects.filter(is_active=True),empty_label="Select City",widget=forms.Select(attrs={'class': 'form-control'})) 
    zone=forms.ModelChoiceField(required=False, 
        queryset=Zone.objects.filter(is_active=True),empty_label="Select Zone",widget=forms.Select(attrs={'class': 'form-control'})) 
    latitude= forms.CharField(required=False,widget=forms.HiddenInput())
    longitude= forms.CharField(required=False,widget=forms.HiddenInput())
    icon = forms.FileField(required=True, label='icon') 
    image = forms.FileField(required=True, label='image') 
   

    class Meta:
        model = Landmark
        fields = ("name","description","state",'city','zone','latitude','longitude','icon','image')


class ProjectForm(forms.ModelForm):
    project_name = forms.CharField(required=True, label='Project Name',max_length=50,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    description = forms.CharField(required=True, label='Description',max_length=80,widget=forms.TextInput(attrs={'class': 'form-control'}))
    state=forms.ModelChoiceField(required=False, 
        queryset=State.objects.filter(is_active=True),empty_label="Select State",widget=forms.Select(attrs={'class': 'form-control'})) 
    city=forms.ModelChoiceField(required=False, 
        queryset=City.objects.filter(is_active=True),empty_label="Select City",widget=forms.Select(attrs={'class': 'form-control'})) 
    zone=forms.ModelChoiceField(required=False, 
        queryset=Zone.objects.filter(is_active=True),empty_label="Select Zone",widget=forms.Select(attrs={'class': 'form-control'})) 
    latitude= forms.CharField(required=False,widget=forms.HiddenInput())
    longitude= forms.CharField(required=False,widget=forms.HiddenInput())
    icon = forms.FileField(required=True, label='icon') 
    image = forms.FileField(required=True, label='image') 
   

    class Meta:
        model = Project
        fields = ("project_name","description","state",'city','zone','latitude','longitude','icon','image')



class DroneVideoForm(forms.ModelForm):
    title = forms.CharField(required=True, label='Title',max_length=50,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    video_url = forms.URLField(required=False, max_length=255,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    #path_color_code = forms.CharField(required=True, label='path_color_code',max_length=7,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))

    description = forms.CharField(required=True, label='Description',max_length=80,widget=forms.TextInput(attrs={'class': 'form-control'}))
    state=forms.ModelChoiceField(required=False, 
        queryset=State.objects.filter(is_active=True),empty_label="Select State",widget=forms.Select(attrs={'class': 'form-control'})) 
    city=forms.ModelChoiceField(required=False, 
        queryset=City.objects.filter(is_active=True),empty_label="Select City",widget=forms.Select(attrs={'class': 'form-control'})) 
    zone=forms.ModelChoiceField(required=False, 
        queryset=Zone.objects.filter(is_active=True),empty_label="Select Zone",widget=forms.Select(attrs={'class': 'form-control'})) 
  
   

    class Meta:
        model = DroneVideo
        fields = ("title","video_url","description","state",'city','zone')


class ZoneForm(forms.ModelForm):
    zone_name = forms.CharField(required=True, label='Title',max_length=50,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    zone_color_code = forms.CharField(required=False, label='zone_color_code',max_length=7,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    name_color_code = forms.CharField(required=False, label='name_color_code',max_length=7,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    population = forms.CharField(required=False, label='population',max_length=20,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    area = forms.CharField(required=False, label='area',max_length=20,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    traffic = forms.CharField(required=False, label='traffic',max_length=20,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'})) 
    state=forms.ModelChoiceField(required=False, 
        queryset=State.objects.filter(is_active=True),empty_label="Select State",widget=forms.Select(attrs={'class': 'form-control'})) 
    city=forms.ModelChoiceField(required=False, 
        queryset=City.objects.filter(is_active=True),empty_label="Select City",widget=forms.Select(attrs={'class': 'form-control'})) 
    
   

    class Meta:
        model = Zone
        fields = ("zone_name","zone_color_code","name_color_code","population","area","traffic","state",'city')


class CityForm(forms.ModelForm): 
    city_name = forms.CharField(required=True, label='Title',max_length=50,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    boundry_color_code = forms.CharField(required=False, label='boundry_color_code',max_length=7,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    map_fill_color_code = forms.CharField(required=False, label='map_fill_color_code',max_length=7,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    center_latitude = forms.CharField(required=False, label='center_latitude',max_length=20,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    center_longitude = forms.CharField(required=False, label='center_longitude',max_length=20,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))
    map_zoom = forms.IntegerField(required=False, label='map_zoom',widget=forms.TextInput(attrs={'class': 'form-control alphaonly'})) 
    map_min_zoom = forms.IntegerField(required=False, label='map_min_zoom',widget=forms.TextInput(attrs={'class': 'form-control alphaonly'})) 
    map_max_zoom = forms.IntegerField(required=False, label='map_max_zoom',widget=forms.TextInput(attrs={'class': 'form-control alphaonly'})) 
    state=forms.ModelChoiceField(required=False, 
        queryset=State.objects.filter(is_active=True),empty_label="Select State",widget=forms.Select(attrs={'class': 'form-control'})) 
    
    
   

    class Meta:
        model = City
        fields = ("city_name","boundry_color_code","map_fill_color_code","center_latitude","center_longitude","map_zoom","map_min_zoom",'map_max_zoom','state')