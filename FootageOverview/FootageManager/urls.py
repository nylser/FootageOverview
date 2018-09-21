from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loc/<int:location_id>/', views.location, name='location'),
    path('cam/<int:camera_id>/', views.camera, name='camera'),
]
