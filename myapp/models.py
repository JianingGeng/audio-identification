# models.py
from django.db import models

import os


class AudioFile(models.Model):
    file = models.FileField(upload_to="audio_files")

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)  # delete file
        super().delete(*args, **kwargs)  # delete db record


class SingleAudioFile(models.Model):
    file = models.FileField(upload_to="single_audio_files/")

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)  # delete file
        super().delete(*args, **kwargs)  # delete db record


class AudioComparisonResult(models.Model):
    source_audio = models.CharField(max_length=255)
    compared_audio = models.CharField(max_length=255)
    similarity = models.BooleanField()

    def __str__(self):
        return (
            f"{self.source_audio} similar to {self.compared_audio}: {self.similarity}"
        )
