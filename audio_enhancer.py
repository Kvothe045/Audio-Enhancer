import librosa
import soundfile as sf
import numpy as np
import os
import noisereduce as nr
from scipy.signal import butter, lfilter
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_input):
    """Extract audio from video file."""
    video = VideoFileClip(video_input)
    audio = video.audio
    if audio is None:
        print("No audio track found in the video file.")
        return None
    audio_path = os.path.splitext(video_input)[0] + '_extracted_audio.wav'
    audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

def normalize_audio(y):
    """Normalize the audio to a consistent volume level."""
    max_amplitude = np.max(np.abs(y))
    if max_amplitude == 0:
        return y
    return y / max_amplitude

def bass_boost(y, sr, gain=6, freq=100):
    """Boost the bass frequencies."""
    b, a = butter(2, freq / (0.5 * sr), btype='low')
    low_freq = lfilter(b, a, y)
    return y + gain * low_freq

def apply_dynamic_compression(y):
    """Apply dynamic range compression."""
    y_compressed = librosa.effects.percussive(y)
    return y_compressed

def enhance_audio(y, sr):
    """Apply enhancements common to all types of audio."""
    # Apply noise reduction
    y_denoised = nr.reduce_noise(y=y, sr=sr)

    # Normalize audio
    y_normalized = normalize_audio(y_denoised)

    # Apply dynamic range compression
    y_compressed = apply_dynamic_compression(y_normalized)

    # Normalize audio again
    y_final = normalize_audio(y_compressed)

    return y_final

def enhance_audio_file(file_path):
    if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
        audio_path = extract_audio_from_video(file_path)
        if audio_path is None:
            raise ValueError("No audio track found in the video file.")
    else:
        audio_path = file_path

    y, sr = librosa.load(audio_path)

    # Enhance the audio
    y_enhanced = enhance_audio(y, sr)

    # Save the enhanced audio
    enhanced_file_path = os.path.join('enhanced', os.path.basename(audio_path))
    sf.write(enhanced_file_path, y_enhanced, sr)

    return enhanced_file_path
