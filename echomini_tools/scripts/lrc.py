import requests
import urllib.parse
from pathlib import Path

out = print

def get(filepath,_out):
    global out
    if _out is not None: out = _out

    out(f"\nGrabbing lyrics: {filepath}")

    metadata = _read_metadata(filepath)
    if metadata is None: return
    synced,lrc = fetch(metadata["artist"], metadata["title"], metadata["album"], metadata["duration"])

    if lrc is not None:
        p = Path(filepath)
        parent_dir = p.parent
        filename_no_ext = p.stem

        if synced:
            outpath = (parent_dir / filename_no_ext).with_suffix(".lrc")
            save(outpath, lrc)
            out(f"Lyrics saved to: {outpath}'")
        else:
            out(f"Lyrics found, but no synced lyrics available: '{metadata['title']} - {metadata['artist']}'")

def fetch(artist, title, album, duration):
    base_url = "https://lrclib.net/api/get"
    params = {}
    if artist:
        params["artist_name"] = artist
    if title:
        params["track_name"] = title
    if album:
        params["album_name"] = album
    if duration:
        params["duration"] = duration

    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = requests.get(url, timeout=40)

    if req.status_code == 200:
        data = req.json()
        synced = data.get("syncedLyrics")
        if synced:
            return True, synced
        else:
            return False, data.get("plainLyrics")
    elif req.status_code == 404:
        out(f"Could not find lyrics for '{title} - {artist}'")
    else:
        out(f"Error {req.status_code} when searching for lyrics for '{title} - {artist}'")

    return None,None

def save(path, lyrics):
    with open(path, "w", encoding="utf-8") as f:
        f.write(lyrics)

from mutagen import File

def _read_metadata(path):
    audio = File(path)
    if audio is None:
        out(f"Unsupported or unreadable file: {path}")
        return None

    cls = audio.__class__.__name__

    title = None
    artist = None
    album = None
    duration = getattr(audio.info, "length", None)

    tags = audio.tags or {}

    match cls:
        case 'MP3' | 'ID3':
            artist = tags.get("TPE1", [None])[0]
            title = tags.get("TIT2", [None])[0]
            album = tags.get("TALB", [None])[0]
        case 'FLAC' | 'OggVorbis':
            artist = tags.get("artist", [None])[0]
            title = tags.get("title", [None])[0]
            album = tags.get("album", [None])[0]
        case 'MP4':
            artist = tags.get("\xa9ART", [None])[0]
            title = tags.get("\xa9nam", [None])[0]
            album = tags.get("\xa9alb", [None])[0]

    if title is None or artist is None:
        out(f"Insufficient tag data for grabbing lyrics: {path}")
        return None

    return {
        "artist": artist,
        "title": title,
        "album": album,
        "duration": duration,
    }