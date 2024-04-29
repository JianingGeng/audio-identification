# myapp/tests/test_task.py

from django.test import TestCase
from myproject.celery import app as celery_app
from celery.contrib.testing.worker import start_worker
from unittest.mock import patch, MagicMock
from django.test import TestCase
from myapp.task import process_audio_task


class CeleryTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Start Celery worker for testing
        cls.celery_worker = start_worker(celery_app)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        # Stop Celery worker after testing
        cls.celery_worker.__exit__(None, None, None)
        super().tearDownClass()


class TestProcessAudioTask(TestCase):
    @patch("myapp.task.process_audio")
    @patch("myapp.models.AudioFile.objects.all")
    @patch("myapp.models.SingleAudioFile.objects.latest")
    def test_process_audio_task(self, mock_latest, mock_all, mock_process_audio):
        # Setup mocks
        # Mock the single audio file retrieval
        mock_single_audio_file = MagicMock()
        mock_single_audio_file.file.path = "/fake/path/single_audio.wav"
        mock_latest.return_value = mock_single_audio_file

        # Mock the retrieval of all audio files
        mock_audio_file = MagicMock()
        mock_audio_file.file.path = "/fake/path/audio_file1.wav"
        mock_all.return_value = [
            mock_audio_file
        ]  # Return a list of one or more mock audio files

        # Setup the return value for the process_audio function
        expected_result = ["Success", "File matched with distance: 0.45"]
        mock_process_audio.return_value = expected_result

        # Execute the task
        results = process_audio_task()

        # Assertions to verify correct behavior
        mock_latest.assert_called_once_with("id")
        mock_all.assert_called_once()
        mock_process_audio.assert_called_once_with(
            "/fake/path/single_audio.wav", ["/fake/path/audio_file1.wav"]
        )
        self.assertEqual(results, expected_result)
