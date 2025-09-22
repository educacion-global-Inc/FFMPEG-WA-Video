#!/bin/bash
#
# FFMPEG Video Converter - Shell Wrapper
#
# This shell script provides a convenient way to run the video converter
# and can be easily executed from any terminal or scheduled as a cron job.
#
# Usage:
#     ./convert.sh
#
# The script will:
# 1. Process all video files in the 'input' directory
# 2. Convert them to MP4 format with WhatsApp-compatible settings
# 3. Save converted files to the 'output' directory
# 4. Log all operations to the 'logs' directory
#

# Set script directory as working directory
cd "$(dirname "$0")"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if ffmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: FFmpeg is required but not installed."
    echo "Please install FFmpeg and try again."
    echo ""
    echo "Installation instructions:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  macOS:         brew install ffmpeg"
    echo "  Windows:       Download from https://ffmpeg.org/"
    exit 1
fi

# Create directories if they don't exist
mkdir -p input output logs

# Check if input directory has any video files
if [ -z "$(find input -maxdepth 1 -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mov" -o -iname "*.mkv" -o -iname "*.wmv" -o -iname "*.flv" -o -iname "*.webm" -o -iname "*.m4v" -o -iname "*.3gp" -o -iname "*.ogv" -o -iname "*.ts" -o -iname "*.mts" -o -iname "*.m2ts" \) 2>/dev/null)" ]; then
    echo "⚠️  No video files found in the 'input' directory."
    echo ""
    echo "Please add video files to the 'input' directory and run the script again."
    echo "Supported formats: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V, 3GP, OGV, TS, MTS, M2TS"
    exit 0
fi

# Display banner
echo "🎬 FFMPEG Video Converter for WhatsApp Format"
echo "=============================================="
echo ""

# Run the Python converter
python3 convert_videos.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Video conversion completed successfully!"
    echo "Check the 'output' directory for converted files."
    echo "Check the 'logs' directory for detailed logs."
else
    echo ""
    echo "❌ Video conversion failed."
    echo "Check the logs for error details."
    exit 1
fi