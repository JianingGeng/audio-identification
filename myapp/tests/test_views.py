# myapp/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from myapp.models import AudioFile, SingleAudioFile


class AudioUploadViewTest(TestCase):

    def test_audio_upload_view_post_valid(self):
        # Prepare a dummy file
        audio = SimpleUploadedFile(
            "test_audio.mp3", b"file_content", content_type="audio/mp3"
        )

        # Get the URL
        url = reverse(
            "upload_audio"
        )  # Make sure 'upload_audio' is the correct name in your urls.py

        # Prepare POST data
        data = {"audio_files": audio}

        # Make a POST request
        response = self.client.post(url, data)

        # Check if the file was saved
        self.assertEqual(AudioFile.objects.count(), 1)
        # If the view redirects after the post, test for redirect
        # self.assertRedirects(response, expected_url, status_code=302)

    def test_audio_upload_view_ajax_post(self):
        # Prepare a dummy file
        audio = SimpleUploadedFile(
            "test_audio.mp3", b"file_content", content_type="audio/mp3"
        )

        # Get the URL
        url = reverse(
            "upload_audio"
        )  # Make sure 'upload_audio' is the correct name in your urls.py

        # Prepare POST data and headers
        data = {"audio_files": audio}
        headers = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}

        # Make an AJAX POST request
        response = self.client.post(url, data, **headers)

        # Check if the AJAX response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "上传成功!"})


# Similarly for SingleAudioUploadView
class SingleAudioUploadViewTest(TestCase):

    def test_single_audio_upload_view_post_valid(self):
        # Prepare a dummy file
        audio = SimpleUploadedFile(
            "test_audio.mp3", b"file_content", content_type="audio/mp3"
        )

        # Get the URL
        url = reverse(
            "upload_single"
        )  # Make sure 'single_audio_upload' is the correct name in your urls.py

        # Prepare POST data
        data = {"audio_file": audio}

        # Make a POST request
        response = self.client.post(url, data)

        # Check if the file was saved
        self.assertEqual(SingleAudioFile.objects.count(), 1)
        # If the view redirects after the post, test for redirect
        # self.assertRedirects(response, expected_url, status_code=302)
