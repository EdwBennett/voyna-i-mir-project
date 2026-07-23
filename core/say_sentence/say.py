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


def validate_paths(lang: str) -> VoiceSpec:
    """Validates that the required files exist for the selected language."""
    if lang not in LANGUAGES:
        print(f"Error: Unsupported language '{lang}'", file=sys.stderr)
        sys.exit(1)
        
    spec = LANGUAGES[lang]
    for path_name, path in [("Piper binary", spec.piper), ("Model", spec.model), ("Config", spec.model_config)]:
        if not path.exists():
            print(f"Error: {path_name} not found at {path}", file=sys.stderr)
            sys.exit(1)
    return spec


def say(*, lang: str, text: str) -> None:
    spec = validate_paths(lang)

    # Convert text to bytes inline so stdout remains raw binary data.
    piper_result = subprocess.run(
        [
            str(spec.piper),
            "--model",
            str(spec.model),
            "--config",
            str(spec.model_config),
            "--output-raw",
        ],
        input=bytes(text, "utf-8"),
        capture_output=True,
        check=True,
    )

    # Play the raw PCM bytes directly from RAM
    subprocess.run(
        ["paplay", "--channels=1", "--rate=22050", "--format=s16le", "--raw"],
        input=piper_result.stdout,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Text-to-speech using Piper and PulseAudio.")
    parser.add_argument(
        "--lang", 
        choices=list(LANGUAGES.keys()), 
        default="en", 
        help="Language voice to use (default: en)"
    )
    parser.add_argument(
        "text", 
        nargs="?", 
        help="Text to speak. If omitted, text will be read from stdin."
    )
    
    args = parser.parse_args()
    
    # Read text from argument or fall back to stdin reading
    if args.text:
        input_text = args.text
    else:
        input_text = sys.stdin.read().strip()
        
    if not input_text:
        print("Error: No input text provided.", file=sys.stderr)
        sys.exit(1)
        
    say(lang=args.lang, text=input_text)


if __name__ == "__main__":
    main()
