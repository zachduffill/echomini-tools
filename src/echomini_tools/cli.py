import argparse
from src.echomini_tools.scripts import lrc, dir, art, flac


def run_cli(args):
    parser = argparse.ArgumentParser()
    cmd = parser.add_subparsers(dest="command", required=True)

    flac_cmd = cmd.add_parser("flac", help="Fix FLAC files")
    flac_cmd.add_argument("target", help="target file (.flac)")

    art_cmd = cmd.add_parser("art", help="Normalise album art")
    art_cmd.add_argument("target", help="target file (.flac .mp3 .ogg .m4a)")

    lrc_cmd = cmd.add_parser("lrc", help="Grab song lyrics")
    lrc_cmd.add_argument("target", help="target file")

    dir_cmd = cmd.add_parser("dir", help="Run fixes on an entire directory")
    dir_cmd.add_argument("target", help="target directory")
    dir_cmd.add_argument("--no-lrc", action="store_true")
    dir_cmd.add_argument("--no-flac", action="store_true")
    dir_cmd.add_argument("--no-art", action="store_true")

    parsed = parser.parse_args(args)

    match parsed.command:
        case "art":
            art.fix(parsed.target)
        case "lrc":
            lrc.get(parsed.target)
        case "flac":
            flac.fix(parsed.target)
        case "dir":
            dir.scan(parsed.target,
                     run_flac = not parsed.no_flac,
                     run_art = not parsed.no_art,
                     run_lrc = not parsed.no_lrc
                     )

