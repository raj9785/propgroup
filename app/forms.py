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
    path_color_code = forms.CharField(required=True, label='path_color_code',max_length=7,widget=forms.TextInput(attrs={'class': 'form-control alphaonly'}))

    description = forms.CharField(required=True, label='Description',max_length=80,widget=forms.TextInput(attrs={'class': 'form-control'}))
    state=forms.ModelChoiceField(required=False, 
        queryset=State.objects.filter(is_active=True),empty_label="Select State",widget=forms.Select(attrs={'class': 'form-control'})) 
    city=forms.ModelChoiceField(required=False, 
        queryset=City.objects.filter(is_active=True),empty_label="Select City",widget=forms.Select(attrs={'class': 'form-control'})) 
    zone=forms.ModelChoiceField(required=False, 
        queryset=Zone.objects.filter(is_active=True),empty_label="Select Zone",widget=forms.Select(attrs={'class': 'form-control'})) 
  
   

    class Meta:
        model = DroneVideo
        fields = ("title","video_url","path_color_code","description","state",'city','zone')


