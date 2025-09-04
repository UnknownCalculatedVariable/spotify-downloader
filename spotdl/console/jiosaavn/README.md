# JioSaavn Integration for spotDL

This extension adds JioSaavn download capabilities to spotDL with a rich, attractive user interface.

## Features

- Download individual songs or entire albums/playlists from JioSaavn
- Beautiful terminal UI with progress bars and information panels
- Automatic embedding of cover art and metadata
- Supports both FLAC and MP3 (320 kbps) formats
- Organizes files by album/artist automatically

## Usage

To download from JioSaavn, use the `jiosaavn` operation:

```bash
spotdl jiosaavn "https://www.jiosaavn.com/song/some-song/XXXXXXXXX"
```

### Options

- `--output DIR`: Specify output directory (default: current directory)
- The format is determined by the `--format` option (mp3 or flac)

### Examples

Download a song:
```bash
spotdl jiosaavn "https://www.jiosaavn.com/song/some-song/XXXXXXXXX"
```

Download an album to a specific directory:
```bash
spotdl --output "/path/to/music" jiosaavn "https://www.jiosaavn.com/album/some-album/XXXXXXXXX"
```

Download in FLAC format:
```bash
spotdl --format flac jiosaavn "https://www.jiosaavn.com/song/some-song/XXXXXXXXX"
```

## Requirements

- `yt-dlp` with JioSaavn extractor support
- `rich` for the UI
- `mutagen` for metadata handling
- `ffmpeg` for audio processing

These should already be installed as part of spotDL.

## Project Structure

```
spotdl/
├── console/
│   ├── jiosaavn/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── downloader.py
│   ├── jiosaavn.py
│   └── entry_point.py  # Updated to include jiosaavn operation
├── utils/
│   └── arguments.py    # Updated to include jiosaavn operation
└── ...
```