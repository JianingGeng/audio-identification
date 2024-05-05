"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# urls.py
from django.http import HttpResponse
from django.urls import path
from myapp.views import AudioUploadView
from myapp.views import SingleAudioUploadView
from myapp.views import show_audio_results, clear_all_models, run_task

urlpatterns = [
    path("upload/", AudioUploadView.as_view(), name="upload_audio"),
    path("upload-single/", SingleAudioUploadView.as_view(), name="upload_single"),
    path("audio-results/", show_audio_results, name="audio-results"),
    path("clear-all/", clear_all_models, name="clear-all"),
    path("run_task/", run_task, name="run_task"),
]
