import argparse
import re
from pathlib import Path


SHORTCODE_RE = re.compile(
    r"{{[<%]\s*(relref|ref)\s+\"(http[^\"]+)\"\s*[>%]}}",
    re.IGNORECASE,
)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    new_text, count = SHORTCODE_RE.subn(lambda m: m.group(2), text)
    if count:
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

    print(f"fixed {total} shortcode links")


if __name__ == "__main__":
    main()
