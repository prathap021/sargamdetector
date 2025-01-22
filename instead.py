import tornado.ioloop
import tornado.web
import tornado.websocket
import numpy as np
import parselmouth  # Praat library for pitch detection

# Define the frequencies for Sargam notes in the Madhya Sthayi (Middle Octave)
SARGAM_FREQUENCIES = {
    "Sa": 261.63,
    "Re": 293.66,
    "Ga": 329.63,
    "Ma": 349.23,
    "Pa": 392.00,
    "Dha": 440.00,
    "Ni": 493.88,
    "sa1":523.25
}

# Define tolerance for pitch comparison (in Hz)
PITCH_TOLERANCE = 10  # Hz

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Connection opened")

    def on_message(self, message):
        try:
            # Assuming `message` is raw PCM audio data
            audio_data = np.frombuffer(message, dtype=np.int16).astype(np.float32) / 32768.0
            print(f"Audio data received, processing {len(audio_data)} samples.")

            # Convert audio data to a Parselmouth sound object
            sound = parselmouth.Sound(audio_data, sampling_frequency=44100)

            # Detect pitch using Parselmouth
            pitch_values = self.detect_pitch(sound)

            # Identify the closest Sargam notes and send results back
            for pitch_value in pitch_values:
                sargam_note = self.identify_sargam_note(pitch_value)
                self.write_message({
                    "pitch": float(pitch_value),
                    "sargam_note": sargam_note
                })

        except Exception as e:
            print(f"Error processing message: {e}")
            self.write_message({"error": f"Invalid data format: {e}"})

    def detect_pitch(self, sound):
        """ Detect pitch values from the given sound object """
        pitch_obj = sound.to_pitch()
        pitch_values = pitch_obj.selected_array['frequency']
        # Filter out unvoiced frames (pitch = 0)
        return pitch_values[pitch_values > 0]

    def identify_sargam_note(self, pitch_value):
        """ Identify the closest Sargam note based on pitch frequency """
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

application = tornado.web.Application([
    (r'/', WebSocketHandler),
])

if __name__ == '__main__':
    application.listen(3001)
    print("WebSocket server started on ws://localhost:3001")
    tornado.ioloop.IOLoop.instance().start()
