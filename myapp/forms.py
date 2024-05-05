# forms.py
from django import forms
from multiupload.fields import MultiMediaField
from django.forms import FileField
from django.core.exceptions import ValidationError


class AudioUploadForm(forms.Form):
    audio_files = MultiMediaField(
        min_num=1,
        max_num=100,  # can change the maximum number of files here
        max_file_size=1024 * 1024 * 20,  # Maximum file size allowed (20MB)
        media_type="audio",  # Restrict file type to audio
    )


class SingleAudioUploadForm(forms.Form):
    audio_files = MultiMediaField(
        min_num=1,
        max_num=1,  # can change the maximum number of files here
        max_file_size=1024 * 1024 * 2,  # Maximum file size allowed (2MB)
        media_type="audio",  # Restrict file type to audio
    )
