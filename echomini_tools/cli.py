import argparse
from echomini_tools.scripts.art import fix

def run_cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("target")
    parsed = parser.parse_args(args)

    print(parsed.command)  # "fix"
    print(parsed.target)   # "path"

    match parsed.command:
        case "art":
            fix(parsed.target)