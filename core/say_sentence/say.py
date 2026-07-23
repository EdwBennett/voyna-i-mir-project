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
        raise ValueError(f"Unsupported language '{lang}'")
        
    spec = LANGUAGES[lang]
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
            if piper_proc.stdout:
                piper_proc.stdout.close()
                
            try:
                piper_proc.communicate(input=text)
            except:
                piper_proc.kill()
                play_proc.kill()
                raise
                
            play_proc.wait()
            piper_proc.wait() # Ensure piper fully finishes and registers exit codes
            
            # Prioritize evaluating the actual consumer tool failure context
            if play_proc.returncode != 0:
                raise subprocess.CalledProcessError(play_proc.returncode, play_cmd)
            if piper_proc.returncode != 0:
                raise subprocess.CalledProcessError(piper_proc.returncode, piper_cmd)

def main() -> None:
    parser = argparse.ArgumentParser(description="Text-to-speech CLI using Piper.")
    parser.add_argument("text", nargs="*", help="Text to speak. If omitted, reads from stdin.")
    parser.add_argument("-l", "--lang", choices=LANGUAGES.keys(), default="en", help="Language voice to use.")
    
    args = parser.parse_args()
    
    if args.text:
        input_text = " ".join(args.text).strip()
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    else:
        input_text = ""

    if not input_text:
        parser.error("No input text provided via arguments or stdin pipeline.")

    try:
        say(lang=args.lang, text=input_text)
    except (ValueError, FileNotFoundError) as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Audio Pipeline Error: Command '{e.cmd}' failed with exit code {e.returncode}.", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        print("\nPlayback interrupted by user.", file=sys.stderr)
        sys.exit(130)

if __name__ == "__main__":
    main()
