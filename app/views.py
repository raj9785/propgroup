from django.shortcuts import render
from .models import Zone,Location,City,TempUser,MobileOtp,UserProfile
from landmark.models import Landmark
from projects.models import Project
from dronevideo.models import DroneVideo,DroneVideoPath
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from urllib.parse import urlparse, parse_qs
import json
from django.contrib.auth import authenticate, logout, login as user_login
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ADDITION
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
import random
from django.utils import timezone
import pytz
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from .forms import LandmarkForm,ProjectForm,DroneVideoForm,ZoneForm,CityForm,LocationForm
def add_time(addminutes):
    itc_timezone = pytz.timezone('Asia/Kolkata')
    current_datetime_itc = timezone.now().astimezone(itc_timezone)
    if addminutes:
        new_datetime_itc = current_datetime_itc + \
            timezone.timedelta(minutes=addminutes)
        return new_datetime_itc
    else:
        return current_datetime_itc
    
def generate_otp():
    return "1234"#str(random.randint(1000, 9999))

def send_otp(mobile):
    expired_at_time = add_time(15)
    otp = generate_otp()
    otpdata = MobileOtp()
    otpdata.mobile = mobile
    otpdata.expired_at = expired_at_time
    otpdata.otp = otp
    otpdata.save()
    send_mobile_otp(mobile, otp)
    return otpdata.id


def send_mobile_otp(mobile, otp):
    response_data={}
    response_data['message'] = "Message sent successfully"
   
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def validate_mobile_number(number):
    pattern = re.compile(r'^[6789]\d{9}$')
    if re.match(pattern, number):
        return True
    else:
        return False




def ajax_login(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        redirect_to=request.POST['redirect_to']
        if username and username:
            user = authenticate(username=username, password=password)
            if user is not None:
                #if user.is_superuser != 1:
                    if user.is_active:
                        user_login(request, user)
                        response_data['error'] = False
                        response_data['message'] = "Logined Successfully"
                        response_data['class'] = "error"
                        response_data['errors'] = ""
                        if redirect_to=="2":
                            redirect_page="action_type=2"
                        elif redirect_to=="3":
                            redirect_page="action_type=3"
                        else:
                           redirect_page=""         
                        response_data['redirect_page'] = redirect_page 
                    else:
                        response_data['error'] = True
                        response_data['message'] = "Account is disabled"
                        response_data['class'] = "success"
                        response_data['errors'] = ""
                # else:
                #     response_data['error'] = True
                #     response_data['message'] = "Access not allowed"
                #     response_data['class'] = "error"
                #     response_data['errors'] = ""
            else:
                response_data['error'] = True
                response_data['message'] = "Wrong email or password"
                response_data['class'] = "error"
                response_data['errors'] = ""
        else:
            response_data['error'] = True
            response_data['message'] = "Enter email and password"
            response_data['class'] = "error"
            response_data['errors'] = ""
    else:
        response_data['error'] = True
        response_data['message'] = "Access not allowed"
        response_data['class'] = "error"
        response_data['errors'] = ""

    return HttpResponse(json.dumps(response_data), content_type="application/json")




def ajax_verify_otp(request):
    response_data = {}
    if request.method == 'POST':
        mobile = request.POST['mobile']
        otp = str(request.POST['otp'])
        verify_type = request.POST['verify_type']
        redirect_to=request.POST['redirect_to']
        try:
            user_data = MobileOtp.objects.filter(
                mobile=mobile, otp=otp).order_by('-id').first()
        except MobileOtp.DoesNotExist:
            user_data = None
        if user_data is not None:
            current_datetime = add_time(0)
            desired_timezone = pytz.timezone('Asia/Kolkata')
            expired_at = user_data.expired_at
            timestamp_in_itc = expired_at.astimezone(desired_timezone)
            # print(current_datetime)
            if current_datetime < timestamp_in_itc:
                if verify_type == "1":
                    try:
                        user = User.objects.get(username=mobile)
                    except User.DoesNotExist:
                        user = None
                    if user is not None:
                        user_login(request, user)
                        MobileOtp.objects.filter(mobile=mobile).delete()
                        response_data['error'] = False
                        response_data['message'] = "Logined Successfully"
                        response_data['class'] = "success"
                        response_data['errors'] = ""
                        if redirect_to=="2":
                            redirect_page="action_type=2"
                        elif redirect_to=="3":
                            redirect_page="action_type=3"
                        else:
                           redirect_page=""         
                        response_data['redirect_page'] = redirect_page
                    else:
                        response_data['error'] = True
                        response_data['message'] = "Your mobile no not registered with Us"
                        response_data['class'] = "error"
                        response_data['errors'] = ""
                else:
                    temp_id = request.POST['temp_id']
                    try:
                        temp_user_data = TempUser.objects.get(id=temp_id)
                    except TempUser.DoesNotExist:
                        temp_user_data = None

                    if temp_user_data is not None:
                        date_joined = add_time(0)
                        userdata = User()
                        userdata.is_active = 1
                        userdata.username = temp_user_data.email
                        userdata.first_name = temp_user_data.name
                        userdata.password = temp_user_data.password
                        userdata.is_staff = 0
                        userdata.date_joined = date_joined
                        userdata.email = temp_user_data.email
                        userdata.save()
                        userprofile = UserProfile()
                        userprofile.user = userdata
                        userprofile.mobile = temp_user_data.mobile
                        userprofile.updated_at = date_joined
                        userprofile.save()
                        user_login(request, userdata)
                        MobileOtp.objects.filter(mobile=mobile).delete()
                        TempUser.objects.filter(id=temp_id).delete()
                        response_data['error'] = False
                        response_data['message'] = "Logined Successfully"
                        response_data['class'] = "success"
                        response_data['errors'] = ""
                    else:
                        response_data['error'] = True
                        response_data['message'] = "OTP expired, send OTP again"
                        response_data['class'] = "error"
                        response_data['errors'] = ""

            else:
                response_data['error'] = True
                response_data['message'] = "OTP expired, send OTP again"
                response_data['class'] = "error"
                response_data['errors'] = ""
        else:
            response_data['error'] = True
            response_data['message'] = "Invalid OTP."
            response_data['class'] = "error"
            response_data['errors'] = ""
    else:
        response_data['error'] = True
        response_data['message'] = "Access not allowed"
        response_data['class'] = "error"
        response_data['errors'] = ""

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_register(request):
    response_data = {}
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        password_enc = make_password(password)
        if name == "":
            response_data['error'] = True
            response_data['message'] = "* All fields are mandatory"
            response_data['class'] = "error"
            response_data['errors'] = ""
            response_data['field_name'] = "name"
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        if mobile == "":
            response_data['error'] = True
            response_data['message'] = "* All fields are mandatory"
            response_data['class'] = "error"
            response_data['errors'] = ""
            response_data['field_name'] = "mobile"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            if validate_mobile_number(mobile):
                isvalid = True
            else:
                response_data['error'] = True
                response_data['message'] = "* The mobile number " + \
                    str(mobile)+" is not valid."
                response_data['class'] = "error"
                response_data['errors'] = ""
                response_data['field_name'] = "mobile"
                return HttpResponse(json.dumps(response_data), content_type="application/json")

        if email == "":
            response_data['error'] = True
            response_data['message'] = "* All fields are mandatory"
            response_data['class'] = "error"
            response_data['errors'] = ""
            response_data['field_name'] = "email"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            try:
                validate_email(email)
                # Email is valid
            except ValidationError as e:
                response_data['error'] = True
                response_data['message'] = "* Enter a valid email address"
                response_data['class'] = "error"
                response_data['errors'] = ""
                response_data['field_name'] = "email"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        if password == "":
            response_data['error'] = True
            response_data['message'] = "* All fields are mandatory"
            response_data['class'] = "error"
            response_data['errors'] = ""
            response_data['field_name'] = "password"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            if len(password) < 8:
                response_data['error'] = True
                response_data['message'] = "* Password must be at least 8 characters long."
                response_data['class'] = "error"
                response_data['errors'] = ""
                response_data['field_name'] = "password"
                return HttpResponse(json.dumps(response_data), content_type="application/json")

        try:
            user_data_mobile = User.objects.get(username=mobile)
        except User.DoesNotExist:
            user_data_mobile = None
        if user_data_mobile is None:

            try:
                user_data_email = User.objects.get(email=email)
            except User.DoesNotExist:
                user_data_email = None
            if user_data_email is None:
                userdata = TempUser()
                userdata.name = name
                userdata.mobile = mobile
                userdata.email = email
                userdata.password = password_enc
                userdata.save()
                send_otp(mobile)
                response_data['error'] = False
                response_data['message'] = "OTP Sent"
                response_data['class'] = "error"
                response_data['temp_id'] = userdata.id
                response_data['errors'] = ""
            else:
                response_data['error'] = True
                response_data['message'] = "* Email already registered"
                response_data['class'] = "error"
                response_data['errors'] = ""

        else:
            response_data['error'] = True
            response_data['message'] = "* Mobile number already registered"
            response_data['class'] = "error"
            response_data['errors'] = ""
    else:
        response_data['error'] = True
        response_data['message'] = "* Access not allowed"
        response_data['class'] = "error"
        response_data['errors'] = ""

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_send_otp(request):
    response_data = {}
    if request.method == 'POST':
        mobile = request.POST['username']
        verify_type = request.POST['verify_type']

        if mobile:
            if validate_mobile_number(mobile):
                if verify_type == "1":
                    try:
                        user = User.objects.get(username=mobile)
                    except User.DoesNotExist:
                        user = None
                    if user is None:
                        response_data['error'] = True
                        response_data['message'] = "Your mobile no not registered with Us"
                        response_data['class'] = "error"
                        response_data['errors'] = ""
                        return HttpResponse(json.dumps(response_data), content_type="application/json")
                MobileOtp.objects.filter(mobile=mobile).delete()
                send_otp(mobile)

                response_data['error'] = False
                response_data['message'] = "OTP sent successfully."
                response_data['class'] = "success"
                response_data['mobile'] = mobile
                response_data['errors'] = ""
            else:
                response_data['error'] = True
                response_data['message'] = "The mobile number " + \
                    str(mobile)+" is not valid."
                response_data['class'] = "error"
                response_data['errors'] = ""
        else:
            response_data['error'] = True
            response_data['message'] = "Enter your registered mobile number"
            response_data['class'] = "error"
            response_data['errors'] = ""
    else:
        response_data['error'] = True
        response_data['message'] = "Access not allowed"
        response_data['class'] = "error"
        response_data['errors'] = ""

    return HttpResponse(json.dumps(response_data), content_type="application/json")



def get_youtube_video_id(url):
    video_id = None
    
    if "youtube.com/watch?v=" in url:  # Regular video URL
        video_id = url.split("youtube.com/watch?v=")[1].split("&")[0]
    elif "youtube.com/shorts/" in url:  # Shorts URL
        video_id = url.split("youtube.com/shorts/")[1].split("?")[0]
    elif "youtu.be/" in url:  # Shortened URL
        video_id = url.split("youtu.be/")[1].split("?")[0]
    
    return video_id


# def get_youtube_video_id(url):
#     parsed_url = urlparse(url)
#     query_params = parse_qs(parsed_url.query)
#     return query_params.get('v', [None])[0]

def ajax_get_video_list(request):
    city_id = request.GET.get('city_id') 
    response_data={}
    records = DroneVideo.objects.all().order_by('title').filter(is_active=True,city_id=city_id)
    video_list=""
    if records:
        for index, drone in enumerate(records):
            video_id = get_youtube_video_id(drone.video_url)
            html_data='<iframe src="https://www.youtube.com/embed/'+video_id+'?autoplay=1&mute=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
            if index==0:
               video_list=video_list+'<div class="carousel-item active">'
            else:
               video_list=video_list+'<div class="carousel-item">'    
            video_list=video_list+'<div class="video-container" id="video_container">'+html_data+'</div>'
            video_list=video_list+'<div class="" id="video_title"></div>'
            video_list=video_list+'</div>'
    
    response_data['video_list']=video_list
    return HttpResponse(json.dumps(response_data), content_type="application/json")       


def get_video_list(request):
    records = DroneVideo.objects.all().order_by('title').filter(is_active=True)
    data = {'list': list(records.values("id", "title"))}
    respone = JsonResponse(data)
    return respone

def get_zone_list(city_id=1,zone_id=""):
   
    if zone_id:
        zone_id=int(zone_id)
        zone_list = Zone.objects.filter(is_active=True,city_id=city_id)
        zone_list = zone_list.exclude(id__in=[zone_id,])
    else:
        zone_list = Zone.objects.filter(is_active=True,city_id=city_id)     
    zone_list = zone_list.order_by('sequence_number')
    return zone_list


def get_city_info(city_id=1):
    try:
        city_info = City.objects.get(id=city_id)
    except City.DoesNotExist:
        city_info = None
    return city_info

def ajax_polygons(request):
    city_id = request.GET.get('city_id') 
    type_admin = request.GET.get('type_admin') 
    action_admin = request.GET.get('action_admin') 
    action_id_admin = request.GET.get('action_id_admin') 

    response_data={}
    response_data['zones_with_boundaries'] = get_zones_with_boundaries(city_id,type_admin,action_admin,action_id_admin)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def ajax_location_polygons(request):
    city_id = request.GET.get('city_id') 

    response_data={}
    response_data['location_with_boundaries'] =  get_location_with_boundaries(city_id)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_location_with_boundaries(city_id):
    # Query all active zones
    locations = Location.objects.filter(is_active=True,city_id=city_id)

    # Prepare data to be sent in JSON response
    zones_data = []
    for location in locations:
        # Get all boundary points for the zone, ordered by sequence number
        # boundaries = LocationBoundry.objects.filter(location=location).order_by('sequence_number')
        
        # Format boundary coordinates for the frontend
        #boundary_coords = [{"lat": float(boundary.latitude), "lng": float(boundary.longitude)} for boundary in boundaries]
        
        # Add zone information and its boundaries
        if location.boundry_color_code:
            boundry_color_code=location.boundry_color_code
        else:
            boundry_color_code="" 

        if location.name_color_code:
            name_color_code=location.name_color_code
        else:
            name_color_code=""  

        if location.fill_color_code:
            fill_color_code=location.fill_color_code
        else:
            fill_color_code=""            
      
        

        zones_data.append({
            "id": str(location.id),
            "info": location.location_name,
            "name_color_code":name_color_code,
            "fill_color_code":fill_color_code,
            "boundry_color_code": boundry_color_code,
            "coords": location.boundry_json
        })
    
    return zones_data


def get_zones_with_boundaries(city_id,type_admin,action_admin,action_id_admin):
    # Query all active zones
    zones = Zone.objects.filter(is_active=True,city_id=city_id)
    # if action_admin=="edit" and type_admin=='zone':
    #     action_id_admin=int(action_id_admin)
    #     zones=zones.filter(id=action_id_admin)

    # Prepare data to be sent in JSON response
    zones_data = []
    for zone in zones:
        # Get all boundary points for the zone, ordered by sequence number
        #boundaries = ZoneBoundry.objects.filter(zone=zone).order_by('sequence_number')
        
        # Format boundary coordinates for the frontend
        #boundary_coords = [{"lat": float(boundary.latitude), "lng": float(boundary.longitude)} for boundary in boundaries]
        
        # Add zone information and its boundaries
        if zone.zone_color_code:
            color_code=zone.zone_color_code
        else:
            color_code=""    
        zones_data.append({
            "id": str(zone.id),
            "info": zone.zone_name,
            "name_color_code":zone.name_color_code,
            "population":zone.population,
            "area":zone.area,
            "traffic":zone.traffic,
            "color": color_code,
            "coords": zone.boundry_json,
        })
    
    return zones_data


def ajax_get_markers(request):
    city_id = request.GET.get('city_id') 

    response_data={}
    response_data['markers'] =  get_markers(city_id)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_markers(city_id):
    markers = []
    landmark_list = Landmark.objects.filter(is_active=True,city_id=city_id)
    if landmark_list:
        for landmark in landmark_list:
            if landmark.icon:
               icon =landmark.icon.url
            else:
               icon=""
            if landmark.image:
               image =landmark.image.url
            else:
               image=""   
            markers.append({
                "id": str(landmark.id),
                "type": "landmark",
                "label": landmark.name,
                "lat": float(landmark.latitude),
                "lng": float(landmark.longitude),
                'description':landmark.description,
                'icon':icon,
                'image':image
            })

    project_list = Project.objects.filter(is_active=True,city_id=city_id)
    if project_list:
        for project in project_list:
            if project.icon:
               icon =project.icon.url
            else:
               icon=""
            if project.image:
               image =project.image.url
            else:
               image=""     
            markers.append({
                "id": str(project.id),
                "type": "landmark",
                "label": project.project_name,
                "lat": float(project.latitude),
                "lng": float(project.longitude),
                'description':project.description,
                'icon':icon,
                'image':image
            })    

    return markers   



def ajax_drone_video_paths(request):
    city_id = request.GET.get('city_id') 

    response_data={}
    response_data['drone_video_paths'] =  get_drone_video_paths(city_id)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_drone_video_paths(city_id):
    drones = DroneVideo.objects.filter(is_active=True,city_id=city_id)
    drone_data = []
    video_list=""
    for drone in drones:
        # Get all boundary points for the zone, ordered by sequence number
        #drone_path_list= DroneVideoPath.objects.filter(drone_video=drone).order_by('sequence_number')
        # Format boundary coordinates for the frontend
        #path_coords = [{"lat": float(drone_path.latitude), "lng": float(drone_path.longitude)} for drone_path in drone_path_list]
        # Add zone information and its boundaries
        if drone.path_color_code:
            color_code=drone.path_color_code
        else:
            color_code="" 
        if drone.video_url :    
            video_id = get_youtube_video_id(drone.video_url)
            html_data='<iframe src="https://www.youtube.com/embed/'+video_id+'?autoplay=1&mute=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
            video_list=video_list+'<div class="carousel-item active">'   
            video_list=video_list+'<div class="video-container" id="video_container">'+html_data+'</div>'
            video_list=video_list+'<div class="" id="video_title"></div>'
            video_list=video_list+'</div>'
        else:
           html_data="";  

        
        drone_data.append({
            "id": str(drone.id),
            "info": drone.description,
            "title": drone.title,
            "color": color_code,
            "html_data":video_list,
            "coordinates": drone.path_json,
        })
    
    return drone_data

from shapely.geometry import Point, Polygon
def find_zone(request):
    lat = request.GET.get('lat') 
    lon = request.GET.get('lng') 
    lat=float(lat)
    lon=float(lon)
    response_data = {}
    response_data['error'] = True
    response_data['message'] = "Zone not Found"
    response_data['data'] = {}
    response_data['class'] = "error"
    response_data['errors'] = ""
    zone_list = Zone.objects.filter(is_active=True)
    if zone_list: 
        for zone_data in zone_list:
            polygon_coords=[]
            zone_path_list= zone_data.boundry_json
            polygon_coords = [(float(loc["lng"]), float(loc["lat"])) for loc in zone_path_list]
            polygon = Polygon(polygon_coords)

            # Define the point
            point = Point(lon, lat)

            # Check if the point is inside the polygon
            is_inside = polygon.contains(point)
            print(polygon_coords)
            print(is_inside)
           
            if(is_inside==True):
                zone_info={}
                zone_info['zone_id']=zone_data.id
                zone_info['zone_name']=zone_data.zone_name
                zone_info['state']=zone_data.state.id
                zone_info['city']=zone_data.city.id
                response_data['error'] = False
                response_data['message'] = "Zone Found"
                response_data['data'] = zone_info
                response_data['class'] = "success"
                response_data['errors'] = ""
                return HttpResponse(json.dumps(response_data), content_type="application/json")

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def save_map(request):
    response_data = {}
    userdata = request.user
    if request.user.is_authenticated:
        if request.method == 'POST':
           action_type = request.POST['action_type'] 
           data = request.POST.copy()
           files = request.FILES  # Get uploaded files
           if action_type=="1":
            landmark_form = LandmarkForm(data,files)
            if landmark_form.is_valid():
                landmark = landmark_form.save(commit=False)
                landmark.user_id = userdata.id
                
                landmark.save()
                # data._mutable = _mutable
                response_data['error'] = False
                response_data['message'] = "Request Sent Successfully"
                response_data['class'] = "success"
                response_data['errors'] = ""
            else:
                response_data['error'] = True
                response_data['class'] = 'error'
                response_data['error_type'] = '2'
                response_data['message'] = ""
                response_data['errors'] = landmark_form.errors
           elif action_type=="2":
              project_form = ProjectForm(data,files)
              if project_form.is_valid():
                    project = project_form.save(commit=False)
                    project.user_id = userdata.id
                    
                    project.save()
                    # data._mutable = _mutable
                    response_data['error'] = False
                    response_data['message'] = "Request Sent Successfully"
                    response_data['class'] = "success"
                    response_data['errors'] = ""
              else:
                    response_data['error'] = True
                    response_data['class'] = 'error'
                    response_data['error_type'] = '2'
                    response_data['message'] = ""
                    response_data['errors'] = project_form.errors
           elif action_type=="4":
                latlongs= request.POST['latlongs']
                if latlongs:
                    try:
                        path_coordinates = json.loads(latlongs)
                        if path_coordinates:
                            Zone_form = ZoneForm(data)
                            if Zone_form.is_valid():
                                    zone = Zone_form.save(commit=False)
                                    zone.boundry_json = path_coordinates
                                  
                                    
                                    zone.save()
                                    

                                    response_data['error'] = False
                                    response_data['message'] = "Zone added Successfully"
                                    response_data['class'] = "success"
                                    response_data['errors'] = ""
                            else:
                                    response_data['error'] = True
                                    response_data['class'] = 'error'
                                    response_data['error_type'] = '2'
                                    response_data['message'] = ""
                                    response_data['errors'] = Zone_form.errors
                        
                        
                        else:
                            response_data['error'] = True
                            response_data['message'] = "* Draw Zone on Map"
                            response_data['class'] = "error"
                            response_data['errors'] = ""  

                    except json.JSONDecodeError as e:
                            response_data['error'] = True
                            response_data['message'] = "* Invalid JSON format"
                            response_data['class'] = "error"
                            response_data['errors'] = ""                    
           elif action_type=="5":
                latlongs= request.POST['latlongs']
                if latlongs:
                    try:
                        path_coordinates = json.loads(latlongs)
                        if path_coordinates:
                            City_form = CityForm(data)
                            if City_form.is_valid():
                                    city = City_form.save(commit=False)
                                    city.boundry_json = path_coordinates
                                  
                                    
                                    city.save()
                                    

                                    response_data['error'] = False
                                    response_data['message'] = "City added Successfully"
                                    response_data['class'] = "success"
                                    response_data['errors'] = ""
                            else:
                                    response_data['error'] = True
                                    response_data['class'] = 'error'
                                    response_data['error_type'] = '2'
                                    response_data['message'] = ""
                                    response_data['errors'] = City_form.errors
                        
                        
                        else:
                            response_data['error'] = True
                            response_data['message'] = "* Draw City on Map"
                            response_data['class'] = "error"
                            response_data['errors'] = ""  

                    except json.JSONDecodeError as e:
                            response_data['error'] = True
                            response_data['message'] = "* Invalid JSON format"
                            response_data['class'] = "error"
                            response_data['errors'] = ""  
           elif action_type=="6":
                latlongs= request.POST['latlongs']
                if latlongs:
                    try:
                        path_coordinates = json.loads(latlongs)
                        if path_coordinates:
                            City_form = LocationForm(data)
                            if City_form.is_valid():
                                    city = City_form.save(commit=False)
                                    city.boundry_json = path_coordinates
                                  
                                    
                                    city.save()
                                    

                                    response_data['error'] = False
                                    response_data['message'] = "Location added Successfully"
                                    response_data['class'] = "success"
                                    response_data['errors'] = ""
                            else:
                                    response_data['error'] = True
                                    response_data['class'] = 'error'
                                    response_data['error_type'] = '2'
                                    response_data['message'] = ""
                                    response_data['errors'] = City_form.errors
                        
                        
                        else:
                            response_data['error'] = True
                            response_data['message'] = "* Draw Location on Map"
                            response_data['class'] = "error"
                            response_data['errors'] = ""  

                    except json.JSONDecodeError as e:
                            response_data['error'] = True
                            response_data['message'] = "* Invalid JSON format"
                            response_data['class'] = "error"
                            response_data['errors'] = ""                                     
           else:
                latlongs= request.POST['latlongs']
                if latlongs:
                    try:
                        path_coordinates = json.loads(latlongs)
                        if path_coordinates:
                            drone_video_form = DroneVideoForm(data)
                            if drone_video_form.is_valid():
                                    drone_video = drone_video_form.save(commit=False)
                                    drone_video.user_id = userdata.id
                                    drone_video.path_json = path_coordinates
                                    # zone_path = []
                                    # for index, path_coordinate in enumerate(path_coordinates): 
                                    #         latlng={}
                                    #         latlng['lat'] = path_coordinate['lat']
                                    #         latlng['lng'] = path_coordinate['lng']        
                                    #         zone_path.insert(index, latlng)
                                    
                                    drone_video.save()
                                    # data._mutable = _mutable
                                   
                                    # for index, path_coordinate in enumerate(path_coordinates):    
                                    #     drone_video_path = DroneVideoPath()
                                    #     drone_video_path.drone_video = drone_video
                                    #     drone_video_path.latitude = path_coordinate['lat']
                                    #     drone_video_path.longitude = path_coordinate['lng']
                                    #     drone_video_path.sequence_number = index+1
                                    #     drone_video_path.save() 

                                    response_data['error'] = False
                                    response_data['message'] = "Request Sent Successfully"
                                    response_data['class'] = "success"
                                    response_data['errors'] = ""
                            else:
                                    response_data['error'] = True
                                    response_data['class'] = 'error'
                                    response_data['error_type'] = '2'
                                    response_data['message'] = ""
                                    response_data['errors'] = drone_video_form.errors
                        
                        
                        else:
                            response_data['error'] = True
                            response_data['message'] = "* Draw path on Map"
                            response_data['class'] = "error"
                            response_data['errors'] = ""  

                    except json.JSONDecodeError as e:
                            response_data['error'] = True
                            response_data['message'] = "* Invalid JSON format"
                            response_data['class'] = "error"
                            response_data['errors'] = ""  
        else:
            response_data['error'] = True
            response_data['message'] = "* Invalid access"
            response_data['class'] = "error"
            response_data['errors'] = ""     
 
    else:
        response_data['error'] = True
        response_data['message'] = "* Access not allowed"
        response_data['class'] = "error"
        response_data['errors'] = ""

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_map_form(request):
    context = {}
    city_id = request.GET.get('city_id') 
    action_type = request.GET.get('action_type') 
    if action_type=="1":
        title="Add Landmark"
        context['map_form'] = LandmarkForm()
    elif action_type=="2":
        title="Add Project"
        context['map_form'] = ProjectForm()
    elif action_type=="3":
        title="Add Drone Video"
        context['map_form'] = DroneVideoForm() 
    elif action_type=="4":
        title="Zone Information"
        context['map_form'] = ZoneForm() 
    elif action_type=="5":
        title="City Information"
        context['map_form'] = CityForm() 
    elif action_type=="6":
        title="Location Information"
        context['map_form'] = LocationForm()               
    else:
        title="Zone Information"
        context['map_form'] = ZoneForm()       

    context['page_title'] = title
    context['action_type'] = action_type
    context['city_id'] =city_id
    
   

    return render(request, 'front/includes/map_forms.html', context)


def zones(request):
    context = {}
    if request.user.is_authenticated:
        context['page_name'] = "Zone List"
        listing = Zone.objects.all().order_by('zone_name')
        context['listing'] = listing

       
        action=request.GET.get('action',"")
        id=request.GET.get('id',"")
        record={}
        if action=='edit' and id :
           record = Zone.objects.get(id=id)
        context['record'] = record
        return render(request, 'front/zones.html', context)
    else:
        return redirect("/")


def index(request):
    context = {}
    context['page_name'] = "home"
    zone_list=get_zone_list()
    context['zone_list'] = zone_list
    city_id=1
    #context['zones_with_boundaries'] = get_zones_with_boundaries(city_id)
    #context['markers'] = get_markers(city_id)
    context['drone_video_paths'] = get_drone_video_paths(city_id)
    city_info=get_city_info(city_id)
    if city_info is not None:
        context['city_info'] =city_info
        context['city_id'] =city_id
    else:
        city_info_none={}
        city_info_none['map_zoom']=4
        city_info_none['map_min_zoom']=4
        city_info_none['map_max_zoom']=20
        city_info_none['boundry_color_code']="#000000"
        city_info_none['map_fill_color_code']="#000000"
        city_info_none['center_latitude']="20.5937"
        city_info_none['center_longitude']="78.9629"
        context['city_info'] =city_info_none
        context['city_id'] =city_id

    boundry_color_code="NONE"
    if city_info:
        if city_info.boundry_color_code:
            boundry_color_code=city_info.boundry_color_code
    map_fill_color_code="NONE"
    if city_info:
        if city_info.map_fill_color_code:
            map_fill_color_code=city_info.map_fill_color_code


    context['boundry_color_code'] =boundry_color_code
    context['map_fill_color_code'] =map_fill_color_code

    return render(request, 'front/home.html', context)

def dashboard(request):
    context = {}
    action_type=request.GET.get('action_type',"") 
    action=request.GET.get('action',"")
    type=request.GET.get('type',"")
    id=request.GET.get('id',"")
    if request.user.is_authenticated:
        city_id=1
        context['page_name'] = "dashboard"
        context['action'] = action
        context['type'] = type
        context['action_type'] = action_type
        context['id'] = id
        zone_id=""
        if action=="edit" and type=='zone':
            zone_id=id
        zone_list=get_zone_list(city_id,zone_id)
        #context['zone_list'] = zone_list
        
        #context['zones_with_boundaries'] = get_zones_with_boundaries(city_id)
        #context['markers'] = get_markers(city_id)
        #context['drone_video_paths'] = get_drone_video_paths(city_id)
        city_info=get_city_info(city_id)
        if city_info is not None:
            context['city_info'] =city_info
            context['city_id'] =city_id
        else:
            city_info_none={}
            city_info_none['map_zoom']=4
            city_info_none['map_min_zoom']=4
            city_info_none['map_max_zoom']=20
            city_info_none['boundry_color_code']="#000000"
            city_info_none['map_fill_color_code']="#000000"
            city_info_none['center_latitude']="20.5937"
            city_info_none['center_longitude']="78.9629"
            context['city_info'] =city_info_none
            context['city_id'] =city_id
        boundry_color_code="NONE"
        if city_info:
            if city_info.boundry_color_code:
                boundry_color_code=city_info.boundry_color_code
        map_fill_color_code="NONE"
        if city_info:
            if city_info.map_fill_color_code:
                map_fill_color_code=city_info.map_fill_color_code


        context['boundry_color_code'] =boundry_color_code
        context['map_fill_color_code'] =map_fill_color_code

        return render(request, 'front/home.html', context)
    else:
        return redirect("/")


def zone_list(request):
    records = Zone.objects.all().order_by('zone_name').filter(is_active=True)
    data = {'list': list(records.values("id", "zone_name"))}
    respone = JsonResponse(data)
    return respone

def location_list(request):
    records = Location.objects.all().order_by('location_name').filter(is_active=True)
    data = {'list': list(records.values("id", "location_name"))}
    respone = JsonResponse(data)
    return respone

# def saveroute(request):
#     resp = {}
#     if request.method == 'POST':
#         longitudes = request.POST.getlist('longitudes[]')
#         latitudes = request.POST.getlist('latitudes[]')
#         zone = request.POST.get('zone')
#         if zone:
#             if latitudes and longitudes:
#                 for index, latitude in enumerate(latitudes):
#                     if latitude and longitudes[index]:
#                         route = ZoneBoundry()
#                         route.zone_id = zone
#                         route.latitude = latitude
#                         route.longitude = longitudes[index]
#                         route.sequence_number = index+1
#                         route.save()

#                 resp['error'] = False
#                 resp['message'] = "Zone Boundry added successfully."
#                 resp['class'] = "success"
#                 respone = JsonResponse(resp, safe=False)
#                 return respone
#             else:
#                 resp['error'] = True
#                 resp['message'] = "Please add marker to the map"
#                 resp['class'] = "error"
#                 respone = JsonResponse(resp, safe=False)
#                 return respone
#         else:
#             resp['error'] = True
#             resp['message'] = "Please select Zone"
#             resp['class'] = "error"
#             respone = JsonResponse(resp, safe=False)
#             return respone

#     else:
#         resp['error'] = True
#         resp['message'] = "Please fill all required field"
#         resp['class'] = "error"
#         respone = JsonResponse(resp, safe=False)
#         return respone
    
# def savelocationboundry(request):
#     resp = {}
#     if request.method == 'POST':
#         longitudes = request.POST.getlist('longitudes[]')
#         latitudes = request.POST.getlist('latitudes[]')
#         location = request.POST.get('location')
#         if location:
#             if latitudes and longitudes:
#                 for index, latitude in enumerate(latitudes):
#                     if latitude and longitudes[index]:
#                         route = LocationBoundry()
#                         route.location_id = location
#                         route.latitude = latitude
#                         route.longitude = longitudes[index]
#                         route.sequence_number = index+1
#                         route.save()

#                 resp['error'] = False
#                 resp['message'] = "Location Boundry added successfully."
#                 resp['class'] = "success"
#                 respone = JsonResponse(resp, safe=False)
#                 return respone
#             else:
#                 resp['error'] = True
#                 resp['message'] = "Please add marker to the map"
#                 resp['class'] = "error"
#                 respone = JsonResponse(resp, safe=False)
#                 return respone
#         else:
#             resp['error'] = True
#             resp['message'] = "Please select Location"
#             resp['class'] = "error"
#             respone = JsonResponse(resp, safe=False)
#             return respone

#     else:
#         resp['error'] = True
#         resp['message'] = "Please fill all required field"
#         resp['class'] = "error"
#         respone = JsonResponse(resp, safe=False)
#         return respone    
    
def logout_view(request):
    logout(request)
    return redirect('index')

def save_drone_path_video(request):
    resp = {}
    if request.method == 'POST':
        longitudes = request.POST.getlist('longitudes[]')
        latitudes = request.POST.getlist('latitudes[]')
        drone_video = request.POST.get('drone_video')
        if drone_video:
            if latitudes and longitudes:
                for index, latitude in enumerate(latitudes):
                    if latitude and longitudes[index]:
                        route = DroneVideoPath()
                        route.drone_video_id = drone_video
                        route.latitude = latitude
                        route.longitude = longitudes[index]
                        route.sequence_number = index+1
                        route.save()

                resp['error'] = False
                resp['message'] = "Drone Video Path added successfully."
                resp['class'] = "success"
                respone = JsonResponse(resp, safe=False)
                return respone
            else:
                resp['error'] = True
                resp['message'] = "Please add marker to the map"
                resp['class'] = "error"
                respone = JsonResponse(resp, safe=False)
                return respone
        else:
            resp['error'] = True
            resp['message'] = "Please select Drone Video"
            resp['class'] = "error"
            respone = JsonResponse(resp, safe=False)
            return respone

    else:
        resp['error'] = True
        resp['message'] = "Please fill all required field"
        resp['class'] = "error"
        respone = JsonResponse(resp, safe=False)
        return respone    