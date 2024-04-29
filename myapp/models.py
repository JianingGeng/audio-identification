# models.py
from django.db import models


class AudioFile(models.Model):
    file = models.FileField(upload_to="audio_files")


class SingleAudioFile(models.Model):
    file = models.FileField(upload_to="single_audio_files/")
