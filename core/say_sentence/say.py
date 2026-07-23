#!/usr/bin/env python3
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


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument("--lang", choices=sorted(LANGUAGES.keys()), required=True)
    args = argp.parse_args()

    text = sys.stdin.buffer.read().decode("utf-8")

    if not text.strip():
        print("No input text provided on stdin.", file=sys.stderr)
        sys.exit(1)

    spec = LANGUAGES[args.lang]
    piper = spec["piper"]
    model = spec["model"]
    model_config = spec["model_config"]

    for path_name, path_value in {
        "piper": piper,
        "model": model,
        "model_config": model_config,
    }.items():
        if not path_value.exists():
            print(f"Missing {path_name}: {path_value}", file=sys.stderr)
            sys.exit(2)

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


if __name__ == "__main__":
    main()
    