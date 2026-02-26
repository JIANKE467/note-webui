import argparse
import re
from pathlib import Path


SHORTCODE_RE = re.compile(
    r"{{[<%]\s*(relref|ref)\s+("
    r"\"(http[^\"]+)\"|'(http[^']+)'|(http\S+)"
    r")\s*[>%]}}",
    re.IGNORECASE,
)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    def repl(match: re.Match) -> str:
        return match.group(3) or match.group(4) or match.group(5)

    new_text, count = SHORTCODE_RE.subn(repl, text)
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
