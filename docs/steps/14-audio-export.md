# Step 14: Audio Export (WAV/MP3)

## Objective

Implement high-quality audio export functionality to convert generated MIDI compositions to WAV and MP3 formats for playback and distribution.

## Overview

Currently, the library can generate MIDI files but cannot produce audio directly. This step adds audio synthesis capabilities using FluidSynth with SoundFont samples, then converts to WAV and MP3 formats.

## Dependencies

- **pydub** >= 0.25.0 - Audio processing and format conversion
- **fluidsynth** - System package for MIDI synthesis
- **SoundFont** - GeneralUser GS or similar sample library

## Tasks

### 14.1 SoundFont Management

- [ ] Create `resources/soundfonts/` directory
- [ ] Implement SoundFont downloader module
- [ ] Download GeneralUser GS SoundFont (or use system default)
- [ ] Add fallback to system SoundFont if custom one unavailable
- [ ] Implement SoundFont caching and version checking

### 14.2 Audio Synthesizer Module

- [ ] Rewrite `src/musicgen/io/audio_synthesizer.py` to use FluidSynth properly
- [ ] Implement `AudioSynthesizer` class with:
  - SoundFont loading and configuration
  - MIDI to WAV conversion
  - Instrument program mapping
  - Tempo and timing handling
  - Multi-track mixing
- [ ] Add error handling for missing FluidSynth
- [ ] Implement graceful degradation when FluidSynth unavailable

### 14.3 WAV Export

- [ ] Implement WAV file export from MIDI
- [ ] Add configurable sample rate (44.1kHz, 48kHz)
- [ ] Add stereo/mono options
- [ ] Implement normalization
- [ ] Add fade-in/fade-out options

### 14.4 MP3 Export

- [ ] Implement MP3 encoding from WAV
- [ ] Add configurable bitrate (128, 192, 256, 320 kbps)
- [ ] Add metadata tags (title, artist, album)
- [ ] Handle ffmpeg dependency check
- [ ] Add fallback to WAV-only if ffmpeg unavailable

### 14.5 Integration

- [ ] Update `generate()` function to support audio export
- [ ] Add `export_formats` option: "wav", "mp3", "audio" (both)
- [ ] Update `CompositionResult` to include audio paths
- [ ] Update CLI with audio export options

### 14.6 Testing

- [ ] Create `tests/test_audio_export.py`
- [ ] Test WAV generation from simple melody
- [ ] Test MP3 generation
- [ ] Test multi-track audio mixing
- [ ] Test with and without SoundFont
- [ ] Test graceful error handling

### 14.7 Documentation

- [ ] Update README with audio export instructions
- [ ] Document FluidSynth installation (Ubuntu, macOS, Windows)
- [ ] Add audio export tutorial
- [ ] Document SoundFont options

## Deliverables

- `src/musicgen/io/audio_synthesizer.py` (rewritten)
- `src/musicgen/io/soundfont.py` (new)
- `resources/soundfonts/GeneralUser-GS-v1.471.sf2` (or cached)
- `tests/test_audio_export.py`
- `examples/audio_export_example.py`
- Documentation updates

## Validation

```python
# Test audio export
request = CompositionRequest(
    mood="peaceful",
    duration=30,
    export_formats=["midi", "wav", "mp3"]
)
result = generate(request)

assert result.midi_path is not None
assert result.wav_path is not None
assert result.mp3_path is not None

# Verify files exist and are valid
assert Path(result.wav_path).exists()
assert Path(result.mp3_path).exists()

# Verify WAV can be loaded
import wave
with wave.open(result.wav_path, 'rb') as f:
    assert f.getnchannels() in [1, 2]
    assert f.getframerate() in [44100, 48000]
```

## System Dependencies

### Ubuntu/Debian
```bash
sudo apt install fluidsynth ffmpeg
```

### macOS
```bash
brew install fluidsynth ffmpeg
```

### Windows
- Download FluidSynth from https://github.com/FluidSynth/fluidsynth/releases
- Download ffmpeg from https://ffmpeg.org/download.html

## SoundFont URL

GeneralUser GS SoundFont:
- URL: https://schristiancollins.com/generaluser.php
- File: GeneralUser-GS-v1.471.sf2
- Size: ~30MB
- License: ISC
