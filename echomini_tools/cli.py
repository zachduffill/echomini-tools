import argparse
from echomini_tools.scripts import art, lrc, flac

def run_cli(args):
    parser = argparse.ArgumentParser()
    cmd = parser.add_subparsers(dest="command", required=True)

    flac_cmd = cmd.add_parser("flac", help="Fix FLAC files")
    flac_cmd.add_argument("target", help="target file (.flac)")
    art_cmd = cmd.add_parser("art", help="Normalise album art")
    art_cmd.add_argument("target", help="target file (.flac .mp3 .ogg .m4a)")
    lrc_cmd = cmd.add_parser("lrc", help="Grab song lyrics")
    lrc_cmd.add_argument("target", help="target file")

    parsed = parser.parse_args(args)

    match parsed.command:
        case "art":
            art.fix(parsed.target)
        case "lrc":
            lrc.get(parsed.target)
        case "flac":
            flac.fix(parsed.target)
