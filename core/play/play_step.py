"""
from root/db/voyna_i_mir.sqlite for selected chapter_sequence
    write new-line to stdout
    write chapter_full_name to stdout
    write english_translation to stdout
    wait for space-bar press
    say.py --lang ru --text "<voyna_i_mir_russian>"
    write voyna_i_mir_russian to stdout
    write russian_transliteration to stdout
    wait for space-bar press
    repeat
"""

def play_step(chapter_sequence: int) -> None:


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: uv run db_json.py <chapter_sequence>")
    play_step(int(sys.argv[1]))
