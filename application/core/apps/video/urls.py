from django.contrib import admin
from django.urls import path, include
from core.apps.video.views import stream_response, index, show_drone, audio_generator

urlpatterns = [
    path('', index, name="main"),
    path("show_cam/", show_drone),
    path('stream_response/', stream_response, name="stream_response"),
    path('audio_response/', audio_generator, name="audio_response"),
]