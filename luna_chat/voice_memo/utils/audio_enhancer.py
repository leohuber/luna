from pedalboard.io import AudioFile
from pedalboard import NoiseGate, Compressor, LowShelfFilter, Gain, Pedalboard
import noisereduce as nr
sr=44100

with AudioFile('your_audio.wav').resampled_to(sr) as f:
    audio = f.read(f.frames)
#noisereduction
reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.75)
#enhancing through pedalboard
board = Pedalboard([
    NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
    Compressor(threshold_db=-16, ratio=4),
    LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
    Gain(gain_db=2)
])

effected = board(reduced_noise, sr)