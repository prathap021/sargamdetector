Sargam Detector 🎵 

A Python-based application that detects Sargam (musical notes) from audio files or real-time input. Ideal for Indian classical music enthusiasts and learners who want to analyze musical patterns.
Features

    🎶 Detect Notes: Recognizes and displays musical notes (Sa, Re, Ga, Ma, Pa, Dha, Ni).
    🎙️ Real-time Analysis: Detect notes from live audio input using a microphone.
    ⚡ Fast and Accurate: Optimized algorithms for quick and precise detection.

Prerequisites

Make sure you have Python 3.8 or above installed. The following libraries are required:

    numpy
    librosa
    matplotlib
    pyaudio (for real-time audio analysis)

To install the dependencies, run:

pip install numpy librosa matplotlib pyaudio

Installation

    Clone this repository:

git clone https://github.com/prathap021/sargamdetector

Navigate to the project directory:

cd sargam-detector

Install the dependencies:

    pip install -r requirements.txt

Usage

Start real-time detection with a microphone:

python app.py

How It Works

    Audio Processing: Uses the librosa library to extract audio features like pitch and frequency.
    Note Mapping: Converts frequencies into corresponding Sargam notes based on predefined scales.
    Real-time Processing: Captures audio from the microphone and processes it in chunks for continuous detection.
    
![e5w3oajq](https://github.com/user-attachments/assets/a8bd5698-ac2d-43d1-985d-422b76d4b760)

https://upload.wikimedia.org/score/e/5/e5w3oajqkkbeg91t0jzivgiv1v6z6lt/e5w3oajq.mp3

Contribution

Feel free to contribute by submitting issues or pull requests. Follow these steps to contribute:

    Fork the repository.
    Create a feature branch:

git checkout -b feature/your-feature-name

Commit your changes and push:

    git commit -m "Add your message here"
    git push origin feature/your-feature-name

    Open a pull request.
