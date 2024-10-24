from django.contrib import admin
from django.urls import path, include
from core.apps.video.views import stream_response, index

urlpatterns = [
    path('', index),
    path('stream_response', stream_response, name="stream_response")
]