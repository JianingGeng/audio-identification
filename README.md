# Voice Recognition Project

## Overview
This project is a voice recognition application that identifies specific speakers' voices within uploaded audio files. It leverages the Hugging Face model for voice embedding and recognition tasks.

## Features
- Voice recognition to identify specific speakers.
- Upload interface for audio files.
- Uses Django framework with a simple frontend.

## Model
The project utilizes the `pyannote/embedding` model from Hugging Face, enabling robust speaker recognition capabilities.

## Installation

### Prerequisites
- Django
- Hugging Face Transformers

### Setup
1. Clone the repository:
2. Install required packages:
pip install -r requirements.txt
3. Run migrations:
python manage.py migrate
4. Start the Django server:
python manage.py runserver
## Usage
Navigate to `http://localhost:8000//upload` to access the application. Upload audio files through the web interface and start recognizing speakers.

## License
Distributed under the MIT License. See `LICENSE` for more information.
