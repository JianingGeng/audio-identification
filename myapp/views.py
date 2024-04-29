# views.py
import json
from django.http import JsonResponse
from django.views.generic.edit import FormView
from .forms import AudioUploadForm, SingleAudioUploadForm
from .models import AudioFile, SingleAudioFile


class AudioUploadView(FormView):
    template_name = "audio_form.html"
    form_class = AudioUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["multiple_form"] = self.form_class()
        context["single_form"] = SingleAudioUploadForm()  # Add the single form as well
        return context

    def form_valid(self, form):
        # Save each audio file
        for each_file in form.cleaned_data["audio_files"]:
            AudioFile.objects.create(file=each_file)

        # Check if the request is AJAX
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            data = {"message": "上传成功!"}
            return JsonResponse(data)
        else:
            # If not AJAX, do the default form valid action
            return super(AudioUploadView, self).form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(form.errors, status=400)
        else:
            return super(AudioUploadView, self).form_invalid(form)


class SingleAudioUploadView(FormView):
    template_name = "audio_form.html"
    form_class = SingleAudioUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["single_form"] = self.form_class()
        context["multiple_form"] = AudioUploadForm()  # Add the multiple form as well
        return context

    def form_valid(self, form):
        for each_file in form.cleaned_data["audio_files"]:
            SingleAudioFile.objects.create(file=each_file)

        # Check if the request is AJAX
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            data = {"message": "上传成功!"}
            return JsonResponse(data)
        else:
            # If not AJAX, do the default form valid action
            return super(SingleAudioUploadView, self).form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(form.errors, status=400)
        else:
            return super(SingleAudioUploadView, self).form_invalid(form)
