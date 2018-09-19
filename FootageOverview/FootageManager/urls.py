from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loc/<int:location_id>/', views.location, name='location'),
    path('cam/<int:camera_id>/', views.camera, name='camera'),
    path('cam/<int:camera_id>/<int:year>/', views.year_view, name='year_view'),
    path('cam/<int:camera_id>/<int:year>/<int:month>/',
         views.month_view, name='month_view'),
    path('cam/<int:camera_id>/<int:year>/<int:month>/<int:day>/',
         views.day_view, name='day_view'),
]
