import json
import os
from pathlib import Path

import numpy as np
import torch
from pydub import AudioSegment
from TTS.api import TTS

class TextToSpeech:
    def __init__(self, model, voices):
        os.environ["COQUI_TOS_AGREED"] = "1"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_model = TTS(model, progress_bar=True).to(device)
        self.voices = json.load(open(voices))

    def tts_to_audiosegment(self, text, speaker):
        """Convert TTS directly to AudioSegment without intermediate conversions"""
        sample_rate = self.tts_model.synthesizer.output_sample_rate
        wav_data = self.tts_model.tts(text=text, speaker=speaker, language='en')
        
        # Convert to int16 for AudioSegment
        wav_data = np.asarray(wav_data, dtype=np.float32)
        wav_data_int16 = (wav_data * 32767).astype(np.int16)
        
        # Create AudioSegment directly from numpy array
        audio_segment = AudioSegment(
            wav_data_int16.tobytes(),
            frame_rate=sample_rate,
            sample_width=2,  # 2 bytes for int16
            channels=1
        )
        return audio_segment

    def dict_to_speech_optimized(self, recordings, output_folder):
        total_recordings = len(recordings['recordings'])
        Path(output_folder).mkdir(parents=True, exist_ok=True)
    
        for recording_id, recording in enumerate(recordings['recordings']):
            print(f"[Unstructured Data] Generating recording {recording_id+1}/{total_recordings}...", end='\r', flush=True)
            
            if np.random.random() > 0.5:
                # customer is male, agent is female
                customer_voice = np.random.choice(self.voices['male_voices'])
                agent_voice = np.random.choice(self.voices['female_voices'])
            else:
                # customer is female, agent is male
                customer_voice = np.random.choice(self.voices['female_voices'])
                agent_voice = np.random.choice(self.voices['male_voices'])
                
            speaker_mapping = {
                'customer': customer_voice,
                'agent': agent_voice
            }
            
            # Generate all audio segments
            audio_segments = []
            
            for segment in recording['segments']:
                text = segment['text']
                speaker = speaker_mapping[segment['speaker']]
                
                # Direct conversion to AudioSegment
                audio_segment = self.tts_to_audiosegment(text, speaker)
                audio_segments.append(audio_segment)
            
            # Combine all segments at once
            combined = sum(audio_segments, AudioSegment.empty())
            combined.export(f"{output_folder}/call_center_recording_{recording_id:05d}.wav", format='wav')
        
        return