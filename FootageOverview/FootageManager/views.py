from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Location, Footage, Camera
from .forms import FilterForm
from datetime import datetime


def index(request):
    location_list = Location.objects.all()
    template = loader.get_template('FootageManager/index.html')
    context = {'location_list': location_list}
    return HttpResponse(template.render(context, request))


def location(request, location_id):
    try:
        location = Location.objects.get(pk=location_id)
    except Location.DoesNotExist:
        raise Http404("Question does not exist")
    camera_list = Camera.objects.filter(location=location)
    context = {'camera_list': camera_list, 'location': location}
    return render(request, 'FootageManager/location.html', context=context)


def camera(request, camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)
    data = []
    if request.method == "POST":
        form = FilterForm(request.POST)
        footype = request.POST.get("footype")
        foocause = request.POST.get("foocause")

        date = request.POST.get("date")
        end_time = request.POST.get("end_time")
        start_time = request.POST.get("start_time")
        start_date = datetime.strptime("{}, {}".format(
            date, start_time), "%d.%m.%Y, %H:%M")
        end_date = datetime.strptime("{}, {}".format(
            date, end_time), "%d.%m.%Y, %H:%M")
        data = Footage.objects.order_by('date').filter(
            camera=camera, footype=footype, foocause=foocause,
            date__gte=start_date, date__lte=end_date)
    else:
        form = FilterForm()
    return render(request, 'FootageManager/camera.html',
                  {'camera': camera, 'form': form, 'data': data})


def year_view(request, camera_id, year):
    months = []
    camera = get_object_or_404(Camera, pk=camera_id)
    footage_list = Footage.objects.filter(camera=camera, date__year=year)
    for f in footage_list:
        if f.date.month not in months:
            months.append(f.date.month)
    return render(request, 'FootageManager/year_view.html',
                  {'camera_id': camera_id, 'year': year, 'month_list': months})


def month_view(request, camera_id, year, month):
    pass


def day_view(request, camera_id, year, day, month):
    pass
