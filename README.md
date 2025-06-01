# Shutup 🤫

A Python script that automatically removes silent parts from video files using FFmpeg. Perfect for cleaning up recordings, presentations, or any video content with unwanted silent sections.

## Features

- 🎵 **Automatic silence detection** - Identifies silent regions in video files
- ✂️ **Smart editing** - Removes silence while preserving audio/video sync
- 🚀 **Simple usage** - Single command to process any video file
- 🔧 **Configurable** - Uses FFmpeg's powerful silencedetect filter
- 📁 **Preserves original** - Creates new output file without modifying the original

## Requirements

- Python 3.6+
- FFmpeg (must be installed and available in PATH)

## Installation

1. **Install FFmpeg** (if not already installed):

   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

   **macOS (with Homebrew):**
   ```bash
   brew install ffmpeg
   ```

   **Windows:**
   Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

2. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/shutup.git
   cd shutup
   ```

3. **Make the script executable:**
   ```bash
   chmod +x shutup.py
   ```

## Usage

### Basic Usage

```bash
python3 shutup.py input_video.mp4
```

or if made executable:

```bash
./shutup.py input_video.mp4
```

### Example

```bash
# Process a recording with silent parts
python3 shutup.py my_presentation.mp4

# Output will be saved as: outfile_my_presentation.mp4
```

## How It Works

1. **Silence Detection**: Uses FFmpeg's `silencedetect` filter to identify silent regions
   - Silence threshold: -50dB
   - Minimum silence duration: 1 second

2. **Timeline Generation**: Parses the detected silence regions and creates a timeline of non-silent parts

3. **Video Processing**: Uses FFmpeg's `select` and `aselect` filters to extract only the non-silent portions while maintaining sync

## Configuration

The script currently uses these default settings:
- **Silence threshold**: -50dB (fairly sensitive)
- **Minimum silence duration**: 1 second

To modify these settings, edit the `silencedetect` parameters in the `run_silence_detect()` function:

```python
"-af", "silencedetect=n=-30dB:d=2",  # Less sensitive, longer duration
```

## Output

- Original file: `input_video.mp4`
- Processed file: `outfile_input_video.mp4`

The output file contains only the non-silent portions of the original video, with audio and video properly synchronized.

## Supported Formats

Supports any video format that FFmpeg can process, including:
- MP4
- AVI
- MOV
- MKV
- WebM
- And many more

## Error Handling

The script will display an error if:
- FFmpeg is not installed or not in PATH
- No silence regions are detected in the input file
- The input file is corrupted or in an unsupported format

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source. Please add an appropriate license file.

## Troubleshooting

**FFmpeg not found:**
```
Make sure FFmpeg is installed and available in your system PATH
```

**No silence detected:**
```
Try adjusting the silence detection parameters for your specific audio content
```

**Permission denied:**
```bash
chmod +x shutup.py
```

## Acknowledgments

- Built with [FFmpeg](https://ffmpeg.org/) - the powerful multimedia framework
- Inspired by the need to clean up lengthy recordings automatically

---

⭐ If this tool helped you, please consider giving it a star on GitHub! 