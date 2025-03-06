from pathlib import Path
from langchain.schema import output
from pedalboard.io import AudioFile
from pedalboard import NoiseGate, Compressor, LowShelfFilter, Gain, Pedalboard
import noisereduce as nr

# https://medium.com/@joshiprerak123/transform-your-audio-denoise-and-enhance-sound-quality-with-python-using-pedalboard-24da7c1df042


def improve_audio(input_file: Path) -> Path:

    output_file = input_file.with_suffix(".enhanced.mp3")

    with AudioFile(str(input_file)) as f:

        # Make a Pedalboard object, containing multiple audio plugins:
        #reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.75)

        board = Pedalboard([
            NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
            Compressor(threshold_db=-16, ratio=4),
            LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
            Gain(gain_db=2)
        ])

        # Open an audio file to write to:
        with AudioFile(str(output_file), 'w', f.samplerate, f.num_channels, quality=128) as o:

            # Read one second of audio at a time, until the file is empty:
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)

                #noisereduction
                reduced_noise = nr.reduce_noise(y=chunk, sr=f.samplerate, stationary=True, prop_decrease=0.75)

                # Run the audio through our pedalboard:
                effected = board(reduced_noise, f.samplerate, reset=False)

                # Write the output to our output file:
                o.write(effected)
    return output_file