import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import numpy as np
from aubio import pitch

# Define the frequencies for Sargam notes in the Madhya Sthayi (Middle Octave)
SARGAM_FREQUENCIES = {
    "Sa": 261.63,
    "Re": 293.66,
    "Ga": 329.63,
    "Ma": 349.23,
    "Pa": 392.00,
    "Dha": 440.00,
    "Ni": 493.88
}

# Define tolerance for pitch comparison (in Hz)
PITCH_TOLERANCE = 10  # Hz

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Connection opened")
        # Initialize pitch detection (Aubio)
        self.pitch_detector = pitch("default", 2048, 512, 44100)
        self.pitch_detector.set_unit("Hz")
        print("Pitch detector initialized")

    def on_message(self, message):
        try:
            # Assuming `message` is raw PCM audio data in a format like numpy array or list
            audio_data = np.frombuffer(message, dtype=np.int16).astype(np.float32) / 32768.0
            print(f"Audio data received, processing {len(audio_data)} samples.")

            # Process audio samples in chunks of 512 samples
            for i in range(0, len(audio_data), 512):
                chunk = audio_data[i:i + 512]
                if len(chunk) < 512:
                    chunk = np.pad(chunk, (0, 512 - len(chunk)), 'constant')

                # Get the pitch value for this chunk
                pitch_value = self.pitch_detector(chunk)[0]
                print(f"Detected pitch: {pitch_value} Hz for chunk starting at index {i}")

                # Identify the corresponding Sargam note based on pitch
                sargam_note = self.identify_sargam_note(pitch_value)

                # Send the detected pitch and Sargam note back to the client
                self.write_message({
                    "pitch": float(pitch_value),
                    "sargam_note": sargam_note
                })

        except Exception as e:
            print(f"Error processing message: {e}")
            self.write_message({"error": f"Invalid data format: {e}"})

    def identify_sargam_note(self, pitch_value):
        """ Identify the closest Sargam note based on pitch frequency for the middle octave """
        closest_note = None
        min_diff = float('inf')

        # Find the closest matching note within the Sargam frequencies
        for note, freq in SARGAM_FREQUENCIES.items():
            diff = abs(pitch_value - freq)
            if diff < min_diff and diff < PITCH_TOLERANCE:
                closest_note = note
                min_diff = diff

        if closest_note:
            return closest_note
        else:
            return "No matching Sargam note"

    def on_close(self):
        print("Connection closed")

    def check_origin(self, origin):
        return True  # Allow connections from any origin for testing

# Create the Tornado application
application = tornado.web.Application([
    (r'/', WebSocketHandler),
])

if __name__ == '__main__':
    # Dynamically determine the port from the environment variable
    port = int(os.environ.get("PORT", 3000))  # Fallback to 3000 if PORT is not set
    application.listen(port)
    print(f"WebSocket server started on port {port}")
    tornado.ioloop.IOLoop.instance().start()
