# myapp/tests/test_views.py
from multiprocessing.connection import Client
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from myapp.models import AudioFile, SingleAudioFile, AudioComparisonResult
from unittest.mock import Mock, patch
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from unittest.mock import patch, MagicMock


class AudioFileUploadTests(TestCase):
    def setUp(self):
        # Mock the file upload
        self.audio_file = SimpleUploadedFile(
            "test_audio.mp3", b"file_content", content_type="audio/mpeg"
        )

        self.audio_file.size = Mock(return_value=1024)
        self.clear_all_url = reverse("clear-all")
        self.run_task_url = reverse("run_task")
        self.audio_path = "path/to/fake_audio.mp3"
        dummy_file = SimpleUploadedFile(
            "test_audio.mp3", b"dummy content", content_type="audio/mpeg"
        )
        self.single_audio_file = SingleAudioFile.objects.create(file=dummy_file)

    def test_audio_upload_handling(self):
        with patch("django.core.files.storage.default_storage.save") as mock_save:
            mock_save.return_value = (
                "path/to/test_audio.mp3"  # Mock the return value of the save method
            )
            response = self.client.post(
                reverse("upload_audio"),
                {"audio_files": [self.audio_file]},
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            )

            self.assertEqual(response.status_code, 200)
            mock_save.assert_called_once()
            self.assertJSONEqual(
                str(response.content, encoding="utf8"),
                {"message": "Upload successful!"},
            )

    def test_clear_all_data(self):
        # Testing clear all functionality
        AudioFile.objects.create(file=self.audio_file)
        response = self.client.post(
            self.clear_all_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        # Match the expected JSON exactly with the actual output
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"status": "success", "message": "All data deleted successfully!"},
        )
        self.assertEqual(AudioFile.objects.count(), 0)
