# views.py
import json
import os
from django.http import JsonResponse
from django.views.generic.edit import FormView
from .forms import AudioUploadForm, SingleAudioUploadForm
from .models import AudioFile, SingleAudioFile, AudioComparisonResult
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .task import process_audio_task
from django.urls import reverse


class AudioUploadView(FormView):
    template_name = "audio_form.html"
    form_class = AudioUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["multiple_form"] = self.form_class()
        context["single_form"] = SingleAudioUploadForm()
        return context

    def form_valid(self, form):
        # Save each audio file
        for each_file in form.cleaned_data["audio_files"]:
            AudioFile.objects.create(file=each_file)

        # Check if the request is AJAX
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            data = {"message": "Upload successful!"}
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
        context["multiple_form"] = AudioUploadForm()
        return context

    def form_valid(self, form):
        for each_file in form.cleaned_data["audio_files"]:
            SingleAudioFile.objects.create(file=each_file)

        # Check if the request is AJAX
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            data = {"message": "Upload successful!"}
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


def show_audio_results(request):
    results = AudioComparisonResult.objects.all()
    return render(request, "audio_results.html", {"results": results})


@require_http_methods(["POST"])
def clear_all_models(request):
    try:
        # Delete AudioFile instances and associated files
        for audio_file in AudioFile.objects.all():
            if os.path.isfile(audio_file.file.path):
                os.remove(audio_file.file.path)
            audio_file.delete()

        # Delete SingleAudioFile instances and associated files
        for single_audio_file in SingleAudioFile.objects.all():
            if os.path.isfile(single_audio_file.file.path):
                os.remove(single_audio_file.file.path)
            single_audio_file.delete()

        # Delete AudioComparisonResult instances
        AudioComparisonResult.objects.all().delete()

        return JsonResponse(
            {"status": "success", "message": "All data deleted successfully!"}
        )
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": "An error occurred while deleting data"}
        )


def run_task(request):
    # start celery task
    result = process_audio_task()
    # Calling process_audio_task without .delay() to simplify synchronous execution for demonstration purposes
    results_url = request.build_absolute_uri(reverse("audio-results"))

    return JsonResponse(
        {
            "status": "success",
            "message": "Check the result.",
            "results_url": results_url,
        }
    )
