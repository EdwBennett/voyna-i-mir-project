"""dump, as one json entity, to stdout an entire record of voyna_i_mir.sqlite db."""

def db_json(chapter_sequence: int) -> None:

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: uv run db_json.py <chapter_sequence>")
    db_json(int(sys.argv[1]))
