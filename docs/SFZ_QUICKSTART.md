# SFZ Setup Guide for music-gen-lib

## Installing sfizz

### Ubuntu 24.04
```bash
echo 'deb http://download.opensuse.org/repositories/home:/sfztools:/sfizz/xUbuntu_24.04/ /' | sudo tee /etc/apt/sources.list.d/home:sfztools:sfizz.list
curl -fsSL https://download.opensuse.org/repositories/home:sfztools:sfizz/xUbuntu_24.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_sfztools_sfizz.gpg > /dev/null
sudo apt update
sudo apt install sfizz
```

### Ubuntu 22.04
```bash
echo 'deb http://download.opensuse.org/repositories/home:/sfztools:/sfizz/xUbuntu_22.04/ /' | sudo tee /etc/apt/sources.list.d/home:sfztools:sfizz.list
curl -fsSL https://download.opensuse.org/repositories/home:sfztools:sfizz/xUbuntu_22.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_sfztools_sfizz.gpg > /dev/null
sudo apt update
sudo apt install sfizz
```

## Verify Installation
```bash
# Check if sfizz_render is available (bundled with sfizz package)
which sfizz_render || echo "sfizz_render not found - will use fallback"
```

## SFZ Sound Libraries

To get high-quality orchestral sounds, you need SFZ libraries. Here are free options:

### 1. Spitfire LABS (Free)
- [Spitfire LABS](https://www.spitfireaudio.com/a/labs)
- High-quality orchestral instruments, completely free
- Requires account creation
- Download: LABS Instruments (individual plugins or collections)

### 2. Virtual Playing Orchestra (VSCO)
- [VSCO Community Edition](https://virtualplayingorchestra.ca/)
- Free SFZ library for orchestral instruments
- Direct download: https://virtualplayingorchestra.ca/

### 3. Versilian Studios (Free)
- [Versilian Studios](https://versilian.studio/)
- Free VSCO Chamber Orchestra, Trumpets, etc.
- Good quality, free to use

### 4. Sonatina Symphonic Orchestra (SSO)
- Free, included with many Linux DAW installations
- Good starting point for testing

## Directory Setup

After downloading SFZ libraries, organize them:
```bash
mkdir -p ~/sfz/libraries
# Extract downloaded SFZ files to this directory
```

## Configuration

Update `musicgen/config.py` or set environment variable:
```bash
export SFZ_LIBRARIES_PATH=~/sfz/libraries
```

## Testing

After installation, test the pipeline:
```bash
cd music-gen-lib
uv run python examples/test_single.py
```

The output should show "SFZ available: True" instead of falling back to pretty_midi.

## References
- [sfizz GitHub](https://github.com/sfztools/sfizz)
- [sfizz-render README](https://github.com/sfztools/sfizz-render)
- [OBS Download Page](https://software.opensuse.org/download.html?project=home:sfztools:sfizz&package=sfizz)
