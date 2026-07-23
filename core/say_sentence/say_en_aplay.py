#replaced, remove later
"""Command-line text-to-speech using Piper and aplay.

This module provides a command-line interface for converting text from
standard input into spoken audio using the Piper text-to-speech engine
and the ``aplay`` command-line audio player.

The script reads UTF-8 text from stdin, synthesizes speech audio using a
configured Piper voice model, and streams the resulting raw audio data
to ``aplay`` for immediate playback. If no non-whitespace text is
provided on stdin, an error message is written to stderr and the script
exits with a non-zero status code.

Typical usage example:
    echo "Hello, this is Amy speaking." | python3 ./say_en_aplay.py
"""

#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

HOME = Path.home()

PIPER = HOME / ".local/bin/piper"
MODEL = HOME / ".local/share/piper-voices/en/en_US-amy-medium.onnx"
CONFIG = HOME / ".local/share/piper-voices/en/en_US-amy-medium.onnx.json"


def main():
    text = sys.stdin.buffer.read().decode("utf-8")

    if not text.strip():
        print("No input text provided on stdin.", file=sys.stderr)
        sys.exit(1)

    piper_result = subprocess.run(
        [str(PIPER), "--model", str(MODEL), "--config", str(CONFIG), "--output-raw"],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE,
        check=True,
    )

    subprocess.run(
        ["aplay", "--format=S16_LE", "--rate=22050", "--channels=1", "-"],
        input=piper_result.stdout,
        check=True,
    )


if __name__ == "__main__":
    main()
