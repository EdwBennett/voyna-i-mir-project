"""
say.py – text-to-speech ru/en using Piper.
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

HOME = Path.home()


@dataclass(frozen=True)
class VoiceSpec:
    piper: Path
    model: Path
    model_config: Path


LANGUAGES: dict[str, VoiceSpec] = {
    "en": VoiceSpec(
        piper=HOME / ".local/bin/piper",
        model=HOME / ".local/share/piper-voices/en/en_US-amy-medium.onnx",
        model_config=HOME / ".local/share/piper-voices/en/en_US-amy-medium.onnx.json",
    ),
    "ru": VoiceSpec(
        piper=HOME / ".local/bin/piper",
        model=HOME / ".local/share/piper-voices/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx",
        model_config=HOME / ".local/share/piper-voices/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json",
    ),
}


def say(*, lang: str, text: str) -> None:
    spec = validate_paths(lang)

    piper_result = subprocess.run(
        [
            spec.piper,
            "--model",
            spec.model,
            "--config",
            spec.model_config,
            "--output-raw",
        ],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE,
        check=True,
    )

    subprocess.run(
        ["paplay", "--raw", "--channels=1", "--rate=22050", "--format=s16le"],
        input=piper_result.stdout,
        check=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=sorted(LANGUAGES), required=True)
    parser.add_argument("text", nargs="?", help="Text to speak; if omitted, stdin is used.")
    return parser


def read_text(arg_text: str | None) -> str:
    text = arg_text if arg_text is not None else sys.stdin.read()
    if not text.strip():
        raise ValueError("No input text provided.")
    return text


def validate_paths(lang: str) -> VoiceSpec:
    spec = LANGUAGES[lang]
    for path_name, path_value in spec.__dict__.items():
        if not path_value.exists():
            raise FileNotFoundError(f"Missing {path_name}: {path_value}")
    return spec


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    ns = parser.parse_args(argv)

    try:
        text = read_text(ns.text)
        say(lang=ns.lang, text=text)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
    