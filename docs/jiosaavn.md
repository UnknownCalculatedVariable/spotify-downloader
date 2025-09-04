# JioSaavn Integration for spotDL

This document explains how to use the JioSaavn integration in spotDL.

## Overview

The JioSaavn integration adds the ability to download music from JioSaavn with a rich, attractive user interface while leveraging spotDL's existing infrastructure.

## Installation

The JioSaavn integration is built into spotDL, so no additional installation is required beyond the standard spotDL installation.

## Usage

### Command Line Usage

To download from JioSaavn, use the `jiosaavn` operation:

```bash
spotdl jiosaavn "https://www.jiosaavn.com/song/some-song/XXXXXXXXX"
```

You can also specify options like output directory and format:

```bash
spotdl --output "/path/to/music" --format flac jiosaavn "https://www.jiosaavn.com/album/some-album/XXXXXXXXX"
```

### Programmatic Usage

You can also use the JioSaavn functionality programmatically:

```python
from spotdl.download.downloader import Downloader
from spotdl.console.jiosaavn_cmd import jiosaavn

# Create a downloader instance
downloader = Downloader({
    "output": "./downloads",
    "format": "mp3",
    "audio_providers": ["youtube"],
    "lyrics_providers": ["genius"],
    "threads": 4,
})

# Download using JioSaavn functionality
jiosaavn(["https://www.jiosaavn.com/song/some-song/XXXXXXXXX"], downloader)
```

## Features

- Download individual songs or entire albums/playlists from JioSaavn
- Beautiful terminal UI with progress bars and information panels
- Automatic embedding of cover art and metadata
- Supports both FLAC and MP3 (320 kbps) formats
- Organizes files by album/artist automatically

## Requirements

- `yt-dlp` with JioSaavn extractor support
- `rich` for the UI
- `mutagen` for metadata handling
- `ffmpeg` for audio processing

These should already be installed as part of spotDL.

## How It Works

The JioSaavn integration works by:

1. Using yt-dlp to extract information from JioSaavn URLs
2. Processing the metadata to organize files properly
3. Downloading the audio using yt-dlp with appropriate options
4. Displaying progress and information using the rich library
5. Embedding metadata and cover art into the downloaded files

## Supported URL Types

- Individual song URLs
- Album URLs
- Playlist URLs
- Artist URLs (if supported by yt-dlp)

## Customization

You can customize the behavior using standard spotDL options:

- `--output`: Specify the output directory
- `--format`: Choose between mp3 and flac formats
- `--threads`: Control the number of concurrent downloads
- And many other standard spotDL options

## Troubleshooting

If you encounter issues:

1. Make sure you have the latest version of yt-dlp installed
2. Verify that the JioSaavn URL is correct and accessible
3. Check that you have sufficient disk space
4. Ensure ffmpeg is properly installed and accessible

## Example Commands

Download a single song:
```bash
spotdl jiosaavn "https://www.jiosaavn.com/song/some-song/XXXXXXXXX"
```

Download an album:
```bash
spotdl jiosaavn "https://www.jiosaavn.com/album/some-album/XXXXXXXXX"
```

Download in FLAC format:
```bash
spotdl --format flac jiosaavn "https://www.jiosaavn.com/song/some-song/XXXXXXXXX"
```

Download to a specific directory:
```bash
spotdl --output "/home/user/Music" jiosaavn "https://www.jiosaavn.com/song/some-song/XXXXXXXXX"
```