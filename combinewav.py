import wave
import struct

def read_wav(filename):
    with wave.open(filename, 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()

        audio_data = wf.readframes(n_frames)
        audio_data = struct.unpack('<' + 'h' * (len(audio_data) // sampwidth), audio_data)
        
        return list(audio_data), framerate, n_channels

def mix_audio(data1, data2):
    min_length = min(len(data1), len(data2))
    data1 = data1[:min_length]
    data2 = data2[:min_length]

    mixed_data = []
    for s1, s2 in zip(data1, data2):
        mixed_sample = (s1 + s2) // 2
        mixed_data.append(mixed_sample)
    
    return mixed_data

def write_wav(filename, data, framerate, n_channels):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(2)
        wf.setframerate(framerate)
        wf.writeframes(struct.pack('<' + 'h' * len(data), *data))

song1_data, framerate1, channels1 = read_wav('song1.wav') #Replace with file names to combine here
song2_data, framerate2, channels2 = read_wav('song2.wav') #<--------

assert framerate1 == framerate2, "Sample rates should be the same"
assert channels1 == channels2, "Number of channels should be the same"

mixed_data = mix_audio(song1_data, song2_data)

#Output file
write_wav('mixed_song.wav', mixed_data, framerate1, channels1)
