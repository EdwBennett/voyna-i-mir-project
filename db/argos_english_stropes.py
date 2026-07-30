"""Use argos to create a list of english_stropes from the russian_stropes,
then set voyna_i_mir.sqlite db english_stropes for the <chapter_sequence> record
"""


def argos(chapter_sequence: int) -> None:


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: uv run argos_english_stropes.py <chapter_sequence>")
    argos_stropes(int(sys.argv[1]))
