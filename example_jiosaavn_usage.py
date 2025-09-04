#!/usr/bin/env python3
"""
Example script demonstrating JioSaavn integration with spotDL.
This script shows how to use the JioSaavn functionality programmatically.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path so we can import spotdl
sys.path.insert(0, str(Path(__file__).parent))

from spotdl.download.downloader import Downloader
from spotdl.console.jiosaavn_cmd import jiosaavn


def main():
    # Example JioSaavn URL (replace with a real one)
    jiosaavn_url = "https://www.jiosaavn.com/song/example-song/XXXXXXXXX"
    
    # Create a downloader instance with basic settings
    downloader = Downloader({
        "output": "./downloads",
        "format": "mp3",
        "audio_providers": ["youtube"],
        "lyrics_providers": ["genius"],
        "threads": 4,
    })
    
    print("Starting JioSaavn download...")
    print(f"URL: {jiosaavn_url}")
    print(f"Output directory: {downloader.settings['output']}")
    print(f"Format: {downloader.settings['format']}")
    
    # Download using JioSaavn functionality
    # Note: This is just an example - you would need a real JioSaavn URL to test
    try:
        jiosaavn([jiosaavn_url], downloader)
        print("Download completed!")
    except Exception as e:
        print(f"Error during download: {e}")
        print("Note: This is expected if you're using a fake URL for testing.")


if __name__ == "__main__":
    main()