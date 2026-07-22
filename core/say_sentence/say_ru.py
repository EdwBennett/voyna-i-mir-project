#!/usr/bin/env python3
import configparser
import os
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
CONFIG_PATH = Path(os.environ.get("SAY_RU_CONFIG", HOME / ".config" / "say_ru.ini"))

DEFAULT_PIPER = HOME / ".local/bin/piper"
DEFAULT_MODEL = HOME / ".local/share/piper-voices/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx"
DEFAULT_MODEL_CONFIG = HOME / ".local/share/piper-voices/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json"

parser = configparser.ConfigParser()
parser.read(CONFIG_PATH)

section = parser["say_ru"] if parser.has_section("say_ru") else {}

PIPER = Path(os.environ.get("SAY_RU_PIPER", section.get("piper", str(DEFAULT_PIPER))))
MODEL = Path(os.environ.get("SAY_RU_MODEL", section.get("model", str(DEFAULT_MODEL))))
MODEL_CONFIG = Path(os.environ.get("SAY_RU_MODEL_CONFIG", section.get("model_config", str(DEFAULT_MODEL_CONFIG))))

def main():
    text = sys.stdin.buffer.read().decode("utf-8")

    if not text.strip():
        print("No input text provided on stdin.", file=sys.stderr)
        sys.exit(1)

    for path_name, path_value in {
        "piper": PIPER,
        "model": MODEL,
        "model_config": MODEL_CONFIG,
    }.items():
        if not path_value.exists():
            print(f"Missing {path_name}: {path_value}", file=sys.stderr)
            sys.exit(2)

    piper_result = subprocess.run(
        [str(PIPER), "--model", str(MODEL), "--config", str(MODEL_CONFIG), "--output-raw"],
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
    