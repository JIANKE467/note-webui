import argparse
import re
from pathlib import Path


URL_JSON_RE = re.compile(r"^[ \\t]*\"url\"\\s*:\\s*\"http[^\"]+\"\\s*,?\\s*$", re.IGNORECASE)
URL_YAML_RE = re.compile(r"^[ \\t]*url\\s*:\\s*https?://\\S+\\s*$", re.IGNORECASE)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return 0

    end = text.find("\n---", 3)
    if end == -1:
        return 0

    front = text[:end]
    lines = front.splitlines()
    kept = []
    removed = 0
    for line in lines:
        if URL_JSON_RE.match(line) or URL_YAML_RE.match(line):
            removed += 1
            continue
        kept.append(line)

    if removed:
        new_front = "\n".join(kept)
        new_text = new_front + text[end:]
        path.write_text(new_text, encoding="utf-8")
    return removed


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
