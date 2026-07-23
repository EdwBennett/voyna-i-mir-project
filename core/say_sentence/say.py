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

def get_voice_spec(lang: str) -> VoiceSpec:
    match LANGUAGES.get(lang):
        case VoiceSpec() as spec:
            return spec
        case _:
            sys.exit(f"Error: Unsupported language '{lang}'")

def validate_paths(lang: str) -> VoiceSpec:
    """Validates that the required files exist for the selected language."""
    spec = get_voice_spec(lang)
    for name, path in [("Piper binary", spec.piper), ("Model", spec.model), ("Config", spec.model_config)]:
        if not path.exists():
            raise FileNotFoundError(f"{name} not found at {path}")
    return spec

def say(*, lang: str, text: str) -> None:
    """Pipelines text through Piper and plays it via aplay."""
    spec = validate_paths(lang)

    piper_cmd = [
        str(spec.piper),
        "--model", str(spec.model),
        "--config", str(spec.model_config),
        "--output_raw"
    ]
    
    # Using aplay explicitly configured for raw 16-bit Mono Little-Endian PCM at 22050Hz
    play_cmd = ["aplay", "-c", "1", "-r", "22050", "-f", "S16_LE", "-t", "raw"]

    with subprocess.Popen(piper_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) as piper_proc:
        with subprocess.Popen(play_cmd, stdin=piper_proc.stdout) as play_proc:
            if piper_proc.stdin:
                piper_proc.stdin.write(text)
                piper_proc.stdin.close()
            play_proc.wait()
        piper_proc.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text-to-speech using Piper")
    # nargs="?" makes text optional; default=None lets us detect if it was omitted
    parser.add_argument("text", nargs="?", default=None, help="Text to speak (reads from stdin if omitted)")
    parser.add_argument("--lang", default="en", choices=["en", "ru"], help="Language code (default: en)")
    args = parser.parse_args()

    # Read from stdin if no text argument is provided
    if args.text is None:
        if not sys.stdin.isatty():
            input_text = sys.stdin.read().strip()
        else:
            sys.exit("Error: No text provided and no piped input detected.")
    else:
        input_text = args.text

    if not input_text:
        sys.exit("Error: Text input is empty.")

    try:
        say(lang=args.lang, text=input_text)
    except Exception as e:
        sys.exit(f"Error: {e}")
