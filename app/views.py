from django.shortcuts import render
from .models import Zone,ZoneBoundry,Location,LocationBoundry
from landmark.models import Landmark
from projects.models import Project
from dronevideo.models import DroneVideo,DroneVideoPath
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


def get_video_list(request):
    records = DroneVideo.objects.all().order_by('title').filter(is_active=True)
    data = {'list': list(records.values("id", "title"))}
    respone = JsonResponse(data)
    return respone

def get_zone_list(city_id=1):
    zone_list = Zone.objects.filter(is_active=True,city_id=city_id)
    zone_list = zone_list.order_by('sequence_number')
    return zone_list

from django.shortcuts import render
from django.http import JsonResponse
from .models import Zone, ZoneBoundry

def get_zones_with_boundaries(city_id):
    # Query all active zones
    zones = Zone.objects.filter(is_active=True,city_id=city_id)

    # Prepare data to be sent in JSON response
    zones_data = []
    for zone in zones:
        # Get all boundary points for the zone, ordered by sequence number
        boundaries = ZoneBoundry.objects.filter(zone=zone).order_by('sequence_number')
        
        # Format boundary coordinates for the frontend
        boundary_coords = [{"lat": float(boundary.latitude), "lng": float(boundary.longitude)} for boundary in boundaries]
        
        # Add zone information and its boundaries
        zones_data.append({
            "id": str(zone.id),
            "info": zone.zone_name,
            "color": zone.zone_color_code,
            "coords": boundary_coords
        })
    
    return zones_data


def get_markers(city_id):
    markers = []
    landmark_list = Landmark.objects.filter(is_active=True,city_id=city_id)
    if landmark_list:
        for landmark in landmark_list:
            if landmark.icon:
               icon =landmark.icon.url
            else:
               icon=""
            markers.append({
                "id": str(landmark.id),
                "type": "landmark",
                "label": landmark.name,
                "lat": float(landmark.latitude),
                "lng": float(landmark.longitude),
                'description':landmark.description,
                'icon':icon,
            })

    project_list = Project.objects.filter(is_active=True,city_id=city_id)
    if project_list:
        for project in project_list:
            if project.icon:
               icon =project.icon.url
            else:
               icon=""
            markers.append({
                "id": str(project.id),
                "type": "landmark",
                "label": project.project_name,
                "lat": float(project.latitude),
                "lng": float(project.longitude),
                'description':project.description,
                'icon':icon,
            })    

    return markers    


def index(request):
    context = {}
    context['page_name'] = "home"
    zone_list=get_zone_list()
    context['zone_list'] = zone_list
    city_id=1
    context['zones_with_boundaries'] = get_zones_with_boundaries(city_id)
    context['markers'] = get_markers(city_id)
    
    


    return render(request, 'front/home.html', context)

def leafletjs(request):
    context = {}
    context['page_name'] = "home"
    return render(request, 'front/leafletjs.html', context)


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

def saveroute(request):
    resp = {}
    if request.method == 'POST':
        longitudes = request.POST.getlist('longitudes[]')
        latitudes = request.POST.getlist('latitudes[]')
        zone = request.POST.get('zone')
        if zone:
            if latitudes and longitudes:
                for index, latitude in enumerate(latitudes):
                    if latitude and longitudes[index]:
                        route = ZoneBoundry()
                        route.zone_id = zone
                        route.latitude = latitude
                        route.longitude = longitudes[index]
                        route.sequence_number = index+1
                        route.save()

                resp['error'] = False
                resp['message'] = "Zone Boundry added successfully."
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
            resp['message'] = "Please select Zone"
            resp['class'] = "error"
            respone = JsonResponse(resp, safe=False)
            return respone

    else:
        resp['error'] = True
        resp['message'] = "Please fill all required field"
        resp['class'] = "error"
        respone = JsonResponse(resp, safe=False)
        return respone
    
def savelocationboundry(request):
    resp = {}
    if request.method == 'POST':
        longitudes = request.POST.getlist('longitudes[]')
        latitudes = request.POST.getlist('latitudes[]')
        location = request.POST.get('location')
        if location:
            if latitudes and longitudes:
                for index, latitude in enumerate(latitudes):
                    if latitude and longitudes[index]:
                        route = LocationBoundry()
                        route.location_id = location
                        route.latitude = latitude
                        route.longitude = longitudes[index]
                        route.sequence_number = index+1
                        route.save()

                resp['error'] = False
                resp['message'] = "Location Boundry added successfully."
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
            resp['message'] = "Please select Location"
            resp['class'] = "error"
            respone = JsonResponse(resp, safe=False)
            return respone

    else:
        resp['error'] = True
        resp['message'] = "Please fill all required field"
        resp['class'] = "error"
        respone = JsonResponse(resp, safe=False)
        return respone    
    


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