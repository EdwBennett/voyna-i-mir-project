"""say.py – text-to-speech ru/en using Piper."""

import argparse
import subprocess
import sys
from pathlib import Path

HOME = Path.home()

LANGUAGES = {
    "en": {
        "piper": HOME / ".local/bin/piper",
        "model": HOME / ".local/share/piper-voices/en/en_US-amy-medium.onnx",
        "model_config": HOME / ".local/share/piper-voices/en/en_US-amy-medium.onnx.json",
    },
    "ru": {
        "piper": HOME / ".local/bin/piper",
        "model": HOME / ".local/share/piper-voices/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx",
        "model_config": HOME / ".local/share/piper-voices/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json",
    },
}


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=sorted(LANGUAGES.keys()), required=True)
    parser.add_argument("text", nargs="?", help="Text to speak; if omitted, stdin is used.")
    return parser


def say(args):
    if isinstance(args, argparse.Namespace):
        ns = args
    else:
        ns = build_parser().parse_args(args)

    text = ns.text
    if text is None:
        text = sys.stdin.buffer.read().decode("utf-8")

    if not text.strip():
        raise ValueError("No input text provided.")

    spec = LANGUAGES[ns.lang]
    piper = spec["piper"]
    model = spec["model"]
    model_config = spec["model_config"]

    for path_name, path_value in {
        "piper": piper,
        "model": model,
        "model_config": model_config,
    }.items():
        if not path_value.exists():
            raise FileNotFoundError(f"Missing {path_name}: {path_value}")

    piper_result = subprocess.run(
        [str(piper), "--model", str(model), "--config", str(model_config), "--output-raw"],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE,
        check=True,
    )

    subprocess.run(
        ["paplay", "--raw", "--channels=1", "--rate=22050", "--format=s16le"],
        input=piper_result.stdout,
        check=True,
    )


def main(argv=None):
    try:
        say(argv)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
