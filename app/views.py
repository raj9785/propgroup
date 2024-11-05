from django.shortcuts import render

def index(request):
    context = {}
    context['page_name'] = "home"
    return render(request, 'front/home.html', context)
