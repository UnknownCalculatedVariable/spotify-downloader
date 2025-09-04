"""
JioSaavn module for the console.
"""

from typing import List

from spotdl.download.downloader import Downloader

__all__ = ["jiosaavn"]


def jiosaavn(
    query: List[str],
    downloader: Downloader,
) -> None:
    """
    Download songs from JioSaavn with rich UI.

    ### Arguments
    - query: list of JioSaavn URLs to download.
    - downloader: Downloader instance.
    """
    
    # Import the JioSaavn downloader here to avoid circular imports
    from spotdl.console.jiosaavn.downloader import download_jiosaavn
    
    # Get format from downloader settings or default to mp3
    format_type = "mp3"
    if downloader.settings.get("format") == "flac":
        format_type = "flac"
    
    # Call the JioSaavn downloader with rich UI
    download_jiosaavn(query, downloader, format_type)