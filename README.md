# echomini-tools
tools to make your song files more compatible with the snowsky echo mini.
<br/>Supports .FLAC .MP3 .OGG .M4A

- Normalise album art
  - Fixes art not showing
  - re-embeds as 600x600 jpeg
- Fix FLAC incompatibilities
  - fixes "Format not supported!" error
  - reduces blocksize to 4608, downmixes to stereo
- Lyric grabber
  - fetches lyrics from LRCLIB and saves as .lrc
  - WARNING: not recommended to use this in folder mode on a large number of files (100+) at one time, the requests will timeout, and processing the files will take much longer.

## Installation
```bash
pipx install git+https://github.com/zachduffill/echomini-tools.git
```

## CLI
Running echomini-tools normally will launch the GUI.
<br/>If you add arguments it can be run as a CLI.
```bash
echomini-tools flac {path}
```
```bash
echomini-tools art {path}
```
```bash
echomini-tools lrc {path}
```
```bash
echomini-tools dir {path} --no-flac --no-art --no-lrc
```


