from datetime import datetime
import os
import sys
import sounddevice as sd
import numpy as np
import lameenc

class SysRecorder:
    def __init__(self):
        self.samplerate = 44100
        self.channels = 2
        self.frames_per_buffer = 1024
        self.stream = None
        self.frames = []
        self.error_occured = False

    def start_recording(self):
        self.frames = []
        device_info = sd.query_devices()
        default_device = device_info['default_output_device']
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            blocksize=self.frames_per_buffer,
            channels=self.channels,
            dtype=np.int16,
            device=default_device,
            callback=self._record_callback
        )
        self.stream.start()

    def stop_recording(self, file_name):
        self.stream.stop()
        self.stream.close()
        self.save_recording(file_name)

    def save_recording(self, file_name):
        filename = f"{file_name}_sys.mp3"
        with open(filename, 'wb') as mp3_file:
            encoder = lameenc.Encoder()
            encoder.set_bit_rate(192)
            encoder.set_in_sample_rate(self.samplerate)
            encoder.set_channels(self.channels)
            encoder.set_quality(2)

            audio_data = np.concatenate(self.frames)
            mp3_data = encoder.encode(audio_data.flatten())
            mp3_file.write(mp3_data)

            mp3_data = encoder.flush()
            mp3_file.write(mp3_data)

        output_path = 'questionnaires'

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_filename = os.path.join(output_path, filename)
        os.rename(filename, output_filename)

    def _record_callback(self, indata, frames, time, status):
        if status and not self.error_occured:
            print(status, file=sys.stderr)
            self.error_occured = True
        self.frames.append(indata.copy())
