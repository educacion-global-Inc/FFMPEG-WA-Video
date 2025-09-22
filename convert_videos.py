#!/usr/bin/env python3
"""
FFMPEG Video Conversion Tool for WhatsApp Compatible Format

This tool processes video files from an input directory and converts them to 
MP4 format with H.264 video codec and AAC audio codec, making them compatible 
with WhatsApp and other messaging platforms.

Features:
- Cycles through all video files in the input directory
- Skips files that already exist in the output directory
- Maintains original video dimensions
- Converts to MP4 with H.264 video and AAC audio codecs
- Comprehensive logging of all operations
- Clean error handling and reporting

Author: Educacion Global Inc
License: MIT
"""

import os
import sys
import logging
import subprocess
import datetime
from pathlib import Path
from typing import List, Optional, Tuple


class VideoConverter:
    """
    A robust video converter that processes files from input to output directory
    using FFMPEG with WhatsApp-compatible settings.
    """
    
    # Supported video file extensions
    SUPPORTED_EXTENSIONS = {
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', 
        '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts'
    }
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output", log_dir: str = "logs"):
        """
        Initialize the VideoConverter with specified directories.
        
        Args:
            input_dir: Directory containing source video files
            output_dir: Directory for converted video files
            log_dir: Directory for log files
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.log_dir = Path(log_dir)
        
        # Create directories if they don't exist
        self._create_directories()
        
        # Setup logging
        self._setup_logging()
        
        # Statistics tracking
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'skipped_files': 0,
            'failed_files': 0,
            'start_time': None,
            'end_time': None
        }
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [self.input_dir, self.output_dir, self.log_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self) -> None:
        """Setup comprehensive logging configuration."""
        # Create log filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = self.log_dir / f"video_conversion_{timestamp}.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("="*60)
        self.logger.info("FFMPEG Video Converter Started")
        self.logger.info("="*60)
        self.logger.info(f"Input directory: {self.input_dir.absolute()}")
        self.logger.info(f"Output directory: {self.output_dir.absolute()}")
        self.logger.info(f"Log directory: {self.log_dir.absolute()}")
    
    def _get_video_files(self) -> List[Path]:
        """
        Get all supported video files from the input directory.
        
        Returns:
            List of Path objects for supported video files
        """
        video_files = []
        
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                video_files.append(file_path)
        
        # Sort files alphabetically for consistent processing order
        video_files.sort()
        
        self.logger.info(f"Found {len(video_files)} video files in input directory")
        return video_files
    
    def _get_output_path(self, input_file: Path) -> Path:
        """
        Generate the output file path for a given input file.
        
        Args:
            input_file: Path to the input video file
            
        Returns:
            Path object for the output MP4 file
        """
        # Change extension to .mp4 and move to output directory
        output_filename = input_file.stem + ".mp4"
        return self.output_dir / output_filename
    
    def _file_already_processed(self, output_path: Path) -> bool:
        """
        Check if the output file already exists.
        
        Args:
            output_path: Path to the potential output file
            
        Returns:
            True if file exists, False otherwise
        """
        return output_path.exists()
    
    def _get_video_info(self, file_path: Path) -> Optional[dict]:
        """
        Get video information using ffprobe.
        
        Args:
            file_path: Path to the video file
            
        Returns:
            Dictionary with video information or None if failed
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(file_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            import json
            return json.loads(result.stdout)
            
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to get video info for {file_path}: {e}")
            return None
    
    def _convert_video(self, input_path: Path, output_path: Path) -> bool:
        """
        Convert a single video file to MP4 with H.264/AAC codecs.
        
        Args:
            input_path: Path to the input video file
            output_path: Path for the output MP4 file
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            # FFMPEG command for WhatsApp-compatible conversion
            cmd = [
                'ffmpeg',
                '-i', str(input_path),           # Input file
                '-c:v', 'libx264',               # H.264 video codec
                '-c:a', 'aac',                   # AAC audio codec
                '-preset', 'medium',             # Encoding speed/quality balance
                '-crf', '23',                    # Constant Rate Factor (good quality)
                '-movflags', '+faststart',       # Web-optimized MP4
                '-avoid_negative_ts', 'make_zero',  # Fix timestamp issues
                '-y',                            # Overwrite output files
                str(output_path)                 # Output file
            ]
            
            self.logger.info(f"Converting: {input_path.name} -> {output_path.name}")
            self.logger.debug(f"FFMPEG command: {' '.join(cmd)}")
            
            # Run conversion
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            # Log success
            self.logger.info(f"✓ Successfully converted: {input_path.name}")
            if result.stderr:
                self.logger.debug(f"FFMPEG output: {result.stderr}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"✗ Failed to convert {input_path.name}: {e}")
            if e.stderr:
                self.logger.error(f"FFMPEG error: {e.stderr}")
            
            # Clean up partial output file
            if output_path.exists():
                try:
                    output_path.unlink()
                    self.logger.debug(f"Cleaned up partial file: {output_path}")
                except OSError:
                    pass
            
            return False
        
        except Exception as e:
            self.logger.error(f"✗ Unexpected error converting {input_path.name}: {e}")
            return False
    
    def process_videos(self) -> None:
        """
        Main method to process all videos in the input directory.
        """
        self.stats['start_time'] = datetime.datetime.now()
        
        # Get all video files
        video_files = self._get_video_files()
        self.stats['total_files'] = len(video_files)
        
        if not video_files:
            self.logger.warning("No video files found in input directory")
            return
        
        self.logger.info(f"Starting conversion of {len(video_files)} files...")
        self.logger.info("-" * 60)
        
        # Process each video file
        for i, input_file in enumerate(video_files, 1):
            output_file = self._get_output_path(input_file)
            
            self.logger.info(f"[{i}/{len(video_files)}] Processing: {input_file.name}")
            
            # Check if already processed
            if self._file_already_processed(output_file):
                self.logger.info(f"⏭  Skipping {input_file.name} (already exists in output)")
                self.stats['skipped_files'] += 1
                continue
            
            # Get video info for logging
            video_info = self._get_video_info(input_file)
            if video_info:
                # Extract basic info
                format_info = video_info.get('format', {})
                duration = format_info.get('duration', 'unknown')
                size_mb = float(format_info.get('size', 0)) / (1024 * 1024)
                
                video_streams = [s for s in video_info.get('streams', []) if s.get('codec_type') == 'video']
                if video_streams:
                    stream = video_streams[0]
                    resolution = f"{stream.get('width', '?')}x{stream.get('height', '?')}"
                    codec = stream.get('codec_name', 'unknown')
                    
                    self.logger.info(f"  📹 {resolution} | {codec} | {duration}s | {size_mb:.1f}MB")
            
            # Convert the video
            if self._convert_video(input_file, output_file):
                self.stats['processed_files'] += 1
            else:
                self.stats['failed_files'] += 1
        
        # Final statistics
        self._log_final_statistics()
    
    def _log_final_statistics(self) -> None:
        """Log final conversion statistics."""
        self.stats['end_time'] = datetime.datetime.now()
        duration = self.stats['end_time'] - self.stats['start_time']
        
        self.logger.info("=" * 60)
        self.logger.info("CONVERSION COMPLETED")
        self.logger.info("=" * 60)
        self.logger.info(f"Total files found: {self.stats['total_files']}")
        self.logger.info(f"Successfully processed: {self.stats['processed_files']}")
        self.logger.info(f"Skipped (already exists): {self.stats['skipped_files']}")
        self.logger.info(f"Failed conversions: {self.stats['failed_files']}")
        self.logger.info(f"Total processing time: {duration}")
        self.logger.info("=" * 60)


def main():
    """Main entry point for the video converter."""
    try:
        # Initialize converter
        converter = VideoConverter()
        
        # Process all videos
        converter.process_videos()
        
    except KeyboardInterrupt:
        print("\n🛑 Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()