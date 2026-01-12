import argparse
from echomini_tools.scripts import art, lrc, flac

def run_cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["art, lrc, flac"],
        help="which tool to run"
    )
    parser.add_argument(
        "target",
        help="target file (flac,mp3,ogg,m4a)"
    )
    parsed = parser.parse_args(args)

    match parsed.command:
        case "art":
            art.fix(parsed.target)
        case "lrc":
            lrc.get(parsed.target)
        case "flac":
            flac.fix(parsed.target)
