from django.shortcuts import render
from .models import Zone,ZoneBoundry,Location,LocationBoundry
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def index(request):
    context = {}
    context['page_name'] = "home"
    return render(request, 'front/leafletjs.html', context)

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