#!/usr/bin/env python3
"""
Example script demonstrating JioSaavn integration with spotDL.
"""

import argparse
import sys
from pathlib import Path

# Add the project root to the path so we can import spotdl
sys.path.insert(0, str(Path(__file__).parent))

from spotdl.download.downloader import Downloader
from spotdl.console.jiosaavn import jiosaavn


def main():
    parser = argparse.ArgumentParser(description="Example JioSaavn downloader using spotDL")
    parser.add_argument("url", help="JioSaavn URL to download")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--format", choices=["mp3", "flac"], default="mp3", help="Audio format")
    
    args = parser.parse_args()
    
    # Create a downloader instance with basic settings
    downloader = Downloader({
        "output": args.output,
        "format": args.format,
        "audio_providers": ["youtube"],
        "lyrics_providers": ["genius"],
        "threads": 4,
    })
    
    # Download using JioSaavn functionality
    jiosaavn([args.url], downloader)


if __name__ == "__main__":
    main()