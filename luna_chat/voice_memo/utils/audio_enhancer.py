"""Module: audio_enhancer.

This module provides functionality to enhance audio recordings by performing noise reduction
and applying a series of audio effects using the Pedalboard library. It reads an audio file,
reduces noise with the noisereduce library, and processes the audio stream through various plugins
to improve clarity and overall sound quality. The enhanced audio is then saved as a new mp3 file.

Inspired by: https://medium.com/@joshiprerak123/transform-your-audio-denoise-and-enhance-sound-quality-with-python-using-pedalboard-24da7c1df042
"""

from pathlib import Path

import noisereduce as nr
from pedalboard import Compressor, Gain, LowShelfFilter, NoiseGate, Pedalboard
from pedalboard.io import AudioFile


def improve_audio(input_file: Path) -> Path:
    """Enhance an audio file by reducing noise and applying multiple audio effects.

    This function reads an input audio file, reduces noise using a stationary noise reduction algorithm,
    and processes the audio through a chain of audio effects including a noise gate, compressor,
    low-shelf filter, and gain adjustment. The processed audio is then written to a new file with the
    suffix ".enhanced.mp3".

    Arguments:
    ---------
        input_file: The path to the input audio file to be enhanced.

    Returns:
    -------
        Path: The path to the enhanced audio file.

    Note:
        The function processes the audio in one-second chunks. It preserves the original audio properties,
        such as sample rate and number of channels, and produces an output audio file with a quality setting of 128.

    """
    output_file = input_file.with_suffix(".enhanced.mp3")

    with AudioFile(str(input_file)) as f:
        # Make a Pedalboard object, containing multiple audio plugins:
        board = Pedalboard(
            [
                NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
                Compressor(threshold_db=-16, ratio=4),
                LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
                Gain(gain_db=2),
            ],
        )

        # Open an audio file to write to:
        with AudioFile(str(output_file), "w", f.samplerate, f.num_channels, quality=128) as o:
            # Read one second of audio at a time, until the file is empty:
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)

                # noisereduction
                reduced_noise = nr.reduce_noise(y=chunk, sr=f.samplerate, stationary=True, prop_decrease=0.75)

                # Run the audio through our pedalboard:
                effected = board(reduced_noise, f.samplerate, reset=False)

                # Write the output to our output file:
                o.write(effected)
    return output_file
