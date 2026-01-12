import argparse
from echomini_tools.scripts import art, lrc

def run_cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("target")
    parsed = parser.parse_args(args)

    match parsed.command:
        case "art":
            art.fix(parsed.target)
        case "lrc":
            lrc.get(parsed.target)
