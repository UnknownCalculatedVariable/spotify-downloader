"""
JioSaavn download module for spotDL with rich UI.
"""

import re
import subprocess
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich import box

from spotdl.download.downloader import Downloader
from spotdl.types.song import Song

__all__ = ["download_jiosaavn"]

console = Console()

# Regex pattern for yt-dlp progress
progress_line_re = re.compile(
    r"^\[download\]\s+(\d{1,3}\.\d)%\s+of\s+([\d\.]+[KMG]iB)\s+at\s+([\d\.]+[KMG]iB/s)\s+ETA\s+([\d:]+)"
)

def create_header():
    """Create an attractive header for the downloader."""
    header_text = Text("🎵 JioSaavn Music Downloader", style="bold magenta")
    header_text.append(" • High Quality Audio Downloads", style="dim white")
    return Panel(
        Align.center(header_text),
        box=box.DOUBLE,
        border_style="bright_magenta",
        padding=(1, 2)
    )

def create_config_panel(out_dir: Path, format_type: str):
    """Create a configuration panel showing current settings."""
    config_table = Table(show_header=False, box=None, padding=(0, 2))
    config_table.add_column("Setting", style="cyan", width=15)
    config_table.add_column("Value", style="white")
    
    # Format selection with icons
    if format_type == "mp3":
        format_text = "🎵 MP3 (~320 kbps)"
        format_style = "green"
    elif format_type == "flac":
        format_text = "🎶 FLAC (Lossless)"
        format_style = "blue"
    else:
        format_text = "📀 Default"
        format_style = "yellow"
    
    config_table.add_row("📁 Output Dir:", str(out_dir))
    config_table.add_row("🎯 Format:", Text(format_text, style=format_style))
    
    return Panel(
        config_table,
        title="⚙️  Configuration",
        border_style="cyan",
        box=box.ROUNDED
    )

def create_track_info_panel(entry: Dict[str, Any]):
    """Create an information panel for track/album details."""
    title = entry.get("title") or entry.get("track") or "Unknown"
    album = entry.get("album") or entry.get("album_name") or "Unknown Album"
    artists = "; ".join(entry.get("artists", ["Unknown Artist"])) if entry.get("artists") else "Unknown Artist"
    duration = entry.get("duration", 0)
    
    # Format duration
    if duration:
        minutes, seconds = divmod(duration, 60)
        duration_str = f"{int(minutes):02d}:{int(seconds):02d}"
    else:
        duration_str = "Unknown"
    
    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column("Field", style="bright_yellow", width=12)
    info_table.add_column("Value", style="white")
    
    info_table.add_row("🎵 Title:", title)
    info_table.add_row("💿 Album:", album)
    info_table.add_row("👨‍🎤 Artist(s):", artists)
    info_table.add_row("⏱️  Duration:", duration_str)
    
    return Panel(
        info_table,
        title="🎼 Track Information",
        border_style="green",
        box=box.ROUNDED
    )

def create_content_panel(is_playlist: bool, total_tracks: int, url: str):
    """Create content information panel."""
    if is_playlist:
        content = f"📀 **Playlist detected** with **{total_tracks}** tracks\n🔗 Source: {url}"
        title = "📀 Playlist Content"
    else:
        content = f"🎵 **Single track** detected\n🔗 Source: {url}"
        title = "🎵 Track Content"
    
    return Panel(
        content,
        title=title,
        border_style="blue",
        box=box.ROUNDED
    )

def create_stats_panel(total: int, successful: int, failed: int):
    """Create a statistics panel showing download results."""
    success_rate = (successful / total * 100) if total > 0 else 0
    
    # Choose color based on success rate
    if success_rate == 100:
        rate_style = "bright_green"
        rate_icon = "🎉"
    elif success_rate >= 80:
        rate_style = "green"
        rate_icon = "✅"
    elif success_rate >= 50:
        rate_style = "yellow"
        rate_icon = "⚠️"
    else:
        rate_style = "red"
        rate_icon = "❌"
    
    stats_table = Table(show_header=False, box=None, padding=(0, 2))
    stats_table.add_column("Metric", style="bright_blue", width=15)
    stats_table.add_column("Count", justify="center", width=8)
    
    stats_table.add_row("📊 Total Tracks:", str(total))
    stats_table.add_row("✅ Successful:", str(successful))
    stats_table.add_row("❌ Failed:", str(failed))
    stats_table.add_row("📈 Success Rate:", Text(f"{success_rate:.1f}% {rate_icon}", style=rate_style))
    
    return Panel(
        stats_table,
        title="📊 Download Statistics",
        border_style="bright_blue",
        box=box.ROUNDED
    )

def run_stream(cmd):
    """Helper function to stream subprocess output."""
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in proc.stdout:
        yield ("line", line.rstrip("\n"))
    rc = proc.wait()
    yield ("rc", rc)

def download_with_progress(entry_url: str, outtmpl: str, format_type: str, 
                          track_task=None, progress: Optional[Progress]=None) -> int:
    """Download a track with progress visualization."""
    base = [
        "yt-dlp",
        "--ignore-config",
        "--no-part",
        "--prefer-ffmpeg",
        "--embed-thumbnail",
        "--add-metadata",
        "--no-playlist",
        "--extractor-args", "jiosaavn:all",
    ]
    post = []
    if format_type == "mp3":
        post = ["-x", "--audio-format", "mp3", "--audio-quality", "320K"]
    elif format_type == "flac":
        post = ["-x", "--audio-format", "flac"]

    cmd = base + post + ["-o", outtmpl, entry_url]
    
    last_percent = 0.0
    for kind, payload in run_stream(cmd):
        if kind == "line":
            line = payload
            if progress and track_task is not None:
                m = progress_line_re.match(line.strip())
                if m:
                    pct = float(m.group(1))
                    last_percent = pct
                    progress.update(track_task, completed=pct, total=100)
        elif kind == "rc":
            rc = payload
            return rc
    return 1

def sanitize(name: str) -> str:
    """Sanitize a string to be used as a filename."""
    return re.sub(r'[\\/:*?"<>|]+', "_", name).strip()

def pick_artists(meta: dict) -> List[str]:
    """Extract artist names from metadata."""
    if meta.get("artist"):
        return [meta["artist"]]
    if meta.get("artists"):
        if isinstance(meta["artists"], list):
            return [a.get("name", a) if isinstance(a, dict) else str(a) for a in meta["artists"]]
        return [str(meta["artists"])]
    if meta.get("creator"):
        return [meta["creator"]]
    return ["Unknown Artist"]

def choose_outputs(entry: Dict[str, Any], base_out_dir: Path) -> Tuple[Path, str, List[str], str, str, Optional[str]]:
    """Determine output directory and filename based on entry metadata."""
    artist_list = pick_artists(entry)
    artist = "; ".join(artist_list) if artist_list else None
    album = entry.get("album") or entry.get("album_name") or entry.get("playlist") or entry.get("series") or "Unknown Album"
    title = entry.get("title") or entry.get("track") or "Unknown Title"
    tracknum = None
    
    if entry.get("track_number"):
        tracknum = str(entry["track_number"])
    elif entry.get("playlist_index"):
        tracknum = str(entry["playlist_index"])
    elif entry.get("playlist_autonumber"):
        tracknum = str(entry["playlist_autonumber"])

    # For JioSaavn, we'll always use album layout
    subdir = base_out_dir / sanitize(album)
    subdir.mkdir(parents=True, exist_ok=True)

    if tracknum:
        filename = f"{tracknum.zfill(2)} - {sanitize(title)}"
    else:
        if artist:
            filename = f"{sanitize(artist)} - {sanitize(title)}"
        else:
            filename = sanitize(title)

    return subdir, filename, artist_list, album, title, tracknum

def probe_info(url: str) -> Dict[str, Any]:
    """Get detailed info using yt-dlp"""
    cmd = ["yt-dlp", "--ignore-config", "--dump-single-json", url]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        return json.loads(out)
    except subprocess.CalledProcessError:
        # Try with different extractor options
        cmd = ["yt-dlp", "--ignore-config", "--dump-single-json", "--extractor-args", "jiosaavn:all", url]
        try:
            out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
            return json.loads(out)
        except:
            return {}

def download_jiosaavn(
    query: List[str],
    downloader: Downloader,
    format_type: str = "mp3",
    album_layout: bool = True
) -> None:
    """
    Download JioSaavn tracks with rich UI.
    
    ### Arguments
    - query: list of JioSaavn URLs to download
    - downloader: spotDL Downloader instance
    - format_type: audio format to download (mp3 or flac)
    - album_layout: whether to organize files in album folders
    """
    
    for url in query:
        # Display header
        console.print(create_header())
        time.sleep(1)  # Brief pause to show header
        
        # Display configuration
        console.print(create_config_panel(Path(downloader.settings["output"]), format_type))
        time.sleep(1)  # Brief pause to show config
        
        # Processing indicator with status
        with console.status("🔍 Analyzing URL and extracting information...", spinner="dots"):
            time.sleep(0.5)  # Brief processing indication
            info = probe_info(url)
        
        if not info:
            error_panel = Panel(
                "❌ Could not extract information from the provided URL.\nPlease check the URL and try again.",
                title="❌ Error",
                border_style="red",
                box=box.ROUNDED
            )
            console.print(error_panel)
            continue

        is_playlist = info.get("_type") == "playlist" or info.get("n_entries", 0) > 1
        entries = info.get("entries", []) if is_playlist else [info]
        
        # Display content type information
        console.print(create_content_panel(is_playlist, len(entries), url))
        time.sleep(1)  # Brief pause to show content info
        
        # Show track information if available
        if entries and entries[0]:
            console.print(create_track_info_panel(entries[0]))
            time.sleep(1)  # Brief pause to show track info
        
        if is_playlist and not entries:
            error_panel = Panel(
                "❌ No tracks found in the playlist.\nThe playlist might be empty or private.",
                title="❌ Playlist Error",
                border_style="red",
                box=box.ROUNDED
            )
            console.print(error_panel)
            continue

        # Initialize counters
        total_tracks = len(entries)
        successful_downloads = 0
        failed_downloads = 0
        
        # Clear screen and show minimal download interface
        console.clear()
        console.print(f"⬇️  Downloading {total_tracks} track{'s' if total_tracks != 1 else ''}...\n")
        
        # Minimal progress bars for downloads
        with Progress(
            TextColumn("{task.description}"),
            BarColumn(bar_width=30),
            TextColumn("{task.percentage:>5.1f}%"),
            TimeRemainingColumn(),
            console=console,
            transient=True
        ) as prog:

            # Overall progress for playlists
            overall_task = None
            if is_playlist:
                overall_task = prog.add_task("Overall", total=total_tracks)

            for idx, entry in enumerate(entries, start=1):
                if not entry:
                    if overall_task is not None:
                        prog.advance(overall_task, 1)
                    continue

                track_url = entry.get("webpage_url") or entry.get("url") or url
                if not track_url:
                    failed_downloads += 1
                    if overall_task is not None:
                        prog.advance(overall_task, 1)
                    continue

                subdir, filename, artists, album, title, tracknum = choose_outputs(
                    entry, Path(downloader.settings["output"])
                )
                outtmpl = str((subdir / f"{filename}.%(ext)s").as_posix())

                # Track progress with clean naming
                track_name = title[:25] + "..." if len(title) > 25 else title
                track_task = prog.add_task(track_name, total=100)

                rc = download_with_progress(
                    entry_url=track_url,
                    outtmpl=outtmpl,
                    format_type=format_type,
                    track_task=track_task,
                    progress=prog,
                )

                prog.update(track_task, completed=100)
                prog.remove_task(track_task)

                # For JioSaavn, metadata is already embedded by yt-dlp
                # But we can add additional tagging if needed
                ext = "mp3" if format_type == "mp3" else "flac"
                final_path = subdir / f"{filename}.{ext}"
                
                if final_path.exists():
                    successful_downloads += 1
                else:
                    failed_downloads += 1

                if overall_task is not None:
                    prog.advance(overall_task, 1)

        # Show completion statistics with panel
        console.print(create_stats_panel(total_tracks, successful_downloads, failed_downloads))
        time.sleep(2)  # Show stats for 2 seconds
        
        # Final status message with appropriate panel styling
        if successful_downloads == total_tracks:
            success_panel = Panel(
                "🎉 **All downloads completed successfully!**\n"
                f"📁 Files saved to: {downloader.settings['output']}",
                title="✅ Success",
                border_style="bright_green",
                box=box.DOUBLE
            )
            console.print(success_panel)
        elif successful_downloads > 0:
            partial_panel = Panel(
                f"⚠️  **Partial success:** {successful_downloads}/{total_tracks} downloads completed\n"
                f"❌ {failed_downloads} downloads failed\n"
                f"📁 Successful files saved to: {downloader.settings['output']}",
                title="⚠️  Partial Success",
                border_style="yellow",
                box=box.ROUNDED
            )
            console.print(partial_panel)
        else:
            error_panel = Panel(
                "❌ **All downloads failed**\n"
                "Please check your internet connection and try again.",
                title="❌ Download Failed",
                border_style="red",
                box=box.ROUNDED
            )
            console.print(error_panel)
        
        time.sleep(2)  # Show final status for 2 seconds
        
        # Clear to minimal final state
        console.clear()
        console.print(f"Complete: {successful_downloads}/{total_tracks} tracks downloaded to {downloader.settings['output']}")