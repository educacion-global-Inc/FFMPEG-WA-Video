# FFMPEG Video Converter for WhatsApp

A powerful, easy-to-use video conversion tool that processes video files and converts them to WhatsApp-compatible MP4 format using H.264 video codec and AAC audio codec.

## 🎯 Features

- **Batch Processing**: Automatically processes all video files in the input directory
- **Smart Skip Logic**: Skips files that already exist in the output directory to avoid duplicate processing
- **WhatsApp Compatible**: Converts videos to MP4 with H.264 video codec and AAC audio codec
- **Dimension Preservation**: Maintains original video dimensions during conversion
- **Comprehensive Logging**: Detailed logs of all operations with timestamps
- **Clean Code**: Well-documented, maintainable Python code
- **Error Handling**: Robust error handling with detailed error reporting
- **Progress Tracking**: Real-time progress updates and conversion statistics

## 📁 Directory Structure

```
FFMPEG-WA-Video/
├── input/          # Place your source video files here
├── output/         # Converted MP4 files will be saved here
├── logs/           # Conversion logs with timestamps
├── convert.sh      # Shell script wrapper (recommended)
├── convert_videos.py # Main Python conversion script
└── README.md       # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.6+**: Required to run the conversion script
- **FFmpeg**: Required for video processing
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from [https://ffmpeg.org/](https://ffmpeg.org/)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/educacion-global-Inc/FFMPEG-WA-Video.git
   cd FFMPEG-WA-Video
   ```

2. Make scripts executable:
   ```bash
   chmod +x convert.sh convert_videos.py
   ```

### Usage

#### Method 1: Using Shell Script (Recommended)

1. Place your video files in the `input/` directory
2. Run the conversion:
   ```bash
   ./convert.sh
   ```

#### Method 2: Direct Python Script

```bash
python3 convert_videos.py
```

## 📽️ Supported Video Formats

**Input Formats:**
- MP4, AVI, MOV, MKV, WMV, FLV, WebM
- M4V, 3GP, OGV, TS, MTS, M2TS

**Output Format:**
- MP4 with H.264 video codec and AAC audio codec
- Optimized for WhatsApp and other messaging platforms

## 🔧 Conversion Settings

The tool uses optimized FFmpeg settings for WhatsApp compatibility:

- **Video Codec**: H.264 (libx264)
- **Audio Codec**: AAC
- **Quality**: CRF 23 (high quality)
- **Preset**: Medium (balanced speed/quality)
- **Web Optimization**: Fast start for web playback
- **Dimension**: Preserved from original

## 📊 Logging

Each conversion session creates a detailed log file in the `logs/` directory with:

- Timestamp for each operation
- File processing status (success/skip/failure)
- Video information (resolution, codec, duration, file size)
- Conversion statistics
- Error details for failed conversions

Log filename format: `video_conversion_YYYYMMDD_HHMMSS.log`

## 🔍 Example Output

```
🎬 FFMPEG Video Converter for WhatsApp Format
==============================================

2025-01-20 14:30:15,123 - INFO - Found 3 video files in input directory
2025-01-20 14:30:15,123 - INFO - Starting conversion of 3 files...
2025-01-20 14:30:15,124 - INFO - [1/3] Processing: vacation_video.mov
2025-01-20 14:30:15,156 - INFO -   📹 1920x1080 | h264 | 45.2s | 25.3MB
2025-01-20 14:30:18,789 - INFO - ✓ Successfully converted: vacation_video.mov
2025-01-20 14:30:18,790 - INFO - [2/3] Processing: family_dinner.avi
2025-01-20 14:30:18,791 - INFO - ⏭  Skipping family_dinner.avi (already exists in output)
2025-01-20 14:30:18,791 - INFO - [3/3] Processing: birthday_party.mp4
2025-01-20 14:30:18,825 - INFO -   📹 1280x720 | mpeg4 | 30.1s | 18.7MB
2025-01-20 14:30:21,234 - INFO - ✓ Successfully converted: birthday_party.mp4

============================================================
CONVERSION COMPLETED
============================================================
Total files found: 3
Successfully processed: 2
Skipped (already exists): 1
Failed conversions: 0
Total processing time: 0:00:06.110
============================================================

✅ Video conversion completed successfully!
```

## 🛠️ Advanced Usage

### Custom Directories

You can modify the directory paths in the `VideoConverter` class:

```python
converter = VideoConverter(
    input_dir="my_input_folder",
    output_dir="my_output_folder", 
    log_dir="my_logs_folder"
)
```

### Error Handling

The tool handles various error scenarios:
- Missing FFmpeg installation
- Corrupted video files
- Insufficient disk space
- Permission issues

Failed conversions are logged with detailed error information.

## 📋 Requirements

- Python 3.6 or higher
- FFmpeg installed and accessible in PATH
- Sufficient disk space for converted files

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the logs directory for detailed error information

---

**Made with ❤️ by Educacion Global Inc**

*Converting videos to make sharing easier, one file at a time!*