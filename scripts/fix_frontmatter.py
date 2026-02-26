import argparse
import re
from pathlib import Path


URL_RE = re.compile(r"\"url\"\\s*:\\s*\"(http[^\"]+)\"", re.IGNORECASE)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return 0

    end = text.find("\n---", 3)
    if end == -1:
        return 0

    front = text[:end]
    new_front, count = URL_RE.subn(r"\"source_url\": \"\\1\"", front)
    if count:
        new_text = new_front + text[end:]
        path.write_text(new_text, encoding="utf-8")
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="data root directory")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"root not found: {root}")

    total = 0
    for path in root.rglob("*.md"):
        total += fix_file(path)

    print(f"fixed {total} front matter url fields")


if __name__ == "__main__":
    main()
