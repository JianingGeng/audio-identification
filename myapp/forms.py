# forms.py
from django import forms
from multiupload.fields import MultiMediaField
from django.forms import FileField
from django.core.exceptions import ValidationError


class AudioUploadForm(forms.Form):
    audio_files = MultiMediaField(
        min_num=1,
        max_num=10,  # You can change the maximum number of files here
        max_file_size=1024 * 1024 * 10,  # Maximum file size allowed (10MB)
        media_type="audio",  # Restrict file type to audio
    )


class SingleAudioUploadForm(forms.Form):
    audio_files = MultiMediaField(
        min_num=1,
        max_num=1,  # You can change the maximum number of files here
        max_file_size=1024 * 1024 * 10,  # Maximum file size allowed (10MB)
        media_type="audio",  # Restrict file type to audio
    )
