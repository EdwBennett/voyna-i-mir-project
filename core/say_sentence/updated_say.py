"""Text-to-speech helper using Piper for English and Russian."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

HOME = Path.home()
PIPER_BIN = HOME / ".local/bin/piper"
SAMPLE_RATE = 22050
LANGUAGES: dict[str, "VoiceSpec"] = {}


@dataclass(frozen=True, slots=True)
class VoiceSpec:
    model: Path
    model_config: Path


LANGUAGES.update(
    {
        "en": VoiceSpec(
            model=HOME / ".local/share/piper-voices/en/en_US-amy-medium.onnx",
            model_config=HOME / ".local/share/piper-voices/en/en_US-amy-medium.onnx.json",
        ),
        "ru": VoiceSpec(
            model=HOME / ".local/share/piper-voices/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx",
            model_config=HOME / ".local/share/piper-voices/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json",
        ),
    }
)


def get_voice_spec(lang: str) -> VoiceSpec:
    try:
        return LANGUAGES[lang]
    except KeyError as exc:
        raise ValueError(f"Unsupported language: {lang}") from exc


def validate_paths(lang: str) -> VoiceSpec:
    spec = get_voice_spec(lang)
    for name, path in (("Piper binary", PIPER_BIN), ("Model", spec.model), ("Config", spec.model_config)):
        if not path.exists():
            raise FileNotFoundError(f"{name} not found at {path}")
    return spec


def say(*, lang: str, text: str) -> None:
    spec = validate_paths(lang)
    piper_cmd = [
        str(PIPER_BIN),
        "--model",
        str(spec.model),
        "--config",
        str(spec.model_config),
        "--output_raw",
    ]
    play_cmd = [
        "aplay",
        "-c",
        "1",
        "-r",
        str(SAMPLE_RATE),
        "-f",
        "S16_LE",
        "-t",
        "raw",
    ]

    with subprocess.Popen(piper_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as piper_proc:
        with subprocess.Popen(play_cmd, stdin=piper_proc.stdout) as play_proc:
            assert piper_proc.stdin is not None
            assert piper_proc.stdout is not None
            piper_proc.stdin.write(text.encode())
            piper_proc.stdin.close()
            piper_proc.stdout.close()
            play_proc.wait()
        piper_proc.wait()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Text-to-speech using Piper")
    parser.add_argument("text", nargs="?", help="Text to speak; reads stdin when omitted")
    parser.add_argument("--lang", default="en", choices=sorted(LANGUAGES), help="Language code")
    return parser.parse_args(argv)


def read_text(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text.strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("Error: no text provided and no piped input detected.")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    text = read_text(args)
    if not text:
        raise SystemExit("Error: text input is empty.")
    try:
        say(lang=args.lang, text=text)
    except (FileNotFoundError, ValueError, OSError, subprocess.SubprocessError) as exc:
        raise SystemExit(f"Error: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
