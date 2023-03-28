from datetime import datetime
import os
import sys
import sounddevice as sd
import numpy as np
import lameenc

class VoiceRecorder:
    def __init__(self):
        self.samplerate = 44100
        self.channels = 2
        self.frames_per_buffer = 1024
        self.stream = None
        self.frames = []

    def start_recording(self):
        self.frames = []
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            blocksize=self.frames_per_buffer,
            channels=self.channels,
            dtype=np.int16,
            callback=self._callback
        )
        self.stream.start()

    def stop_recording(self, file_name):
        self.stream.stop()
        self.stream.close()
        self.save_recording(file_name)

    def save_recording(self, file_name):
        filename = f"{file_name}_voice.mp3"
        with open(filename, 'wb') as mp3_file:
            encoder = lameenc.Encoder()
            encoder.set_bit_rate(192)
            encoder.set_in_sample_rate(self.samplerate)
            encoder.set_channels(self.channels)
            encoder.set_quality(2)  # 2-highest, 7-fastest

            for frame in self.frames:
                mp3_data = encoder.encode(frame)
                mp3_file.write(mp3_data)

            mp3_data = encoder.flush()
            mp3_file.write(mp3_data)

        output_path = 'questionnaires'

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_filename = os.path.join(output_path, filename)
        os.rename(filename, output_filename)

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.frames.append(indata.copy())
