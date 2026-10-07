import wave
import math
import struct
import os

os.makedirs("sounds", exist_ok=True)

def create_sound(filename, frequency, duration):
    sample_rate = 44100
    amplitude = 16000
    total_samples = int(sample_rate * duration)

    with wave.open(os.path.join("sounds", filename), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        for i in range(total_samples):
            t = i / sample_rate
            envelope = 1 - (i / total_samples)
            value = int(
                amplitude
                * envelope
                * math.sin(2 * math.pi * frequency * t)
            )
            wav.writeframes(struct.pack("<h", value))

create_sound("slice.wav", 900, 0.08)
create_sound("bomb.wav", 180, 0.25)
create_sound("game_over.wav", 100, 0.60)

print("Sound files created successfully.")