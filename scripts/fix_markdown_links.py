import argparse
import re
from pathlib import Path


LINK_RE = re.compile(r"\]\(([^)]+?)\)", re.IGNORECASE)


def fix_link(target: str) -> str:
    lowered = target.lower()
    if lowered.endswith("/index.md"):
        return target[: -len("index.md")]
    if lowered.endswith("\\index.md"):
        return target[: -len("index.md")].replace("\\", "/")
    if lowered == "index.md":
        return "./"
    if lowered == "./index.md":
        return "./"
    return target


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")

    def repl(match: re.Match) -> str:
        target = match.group(1)
        fixed = fix_link(target)
        if fixed == target:
            return match.group(0)
        return f"]({fixed})"

    new_text, count = LINK_RE.subn(repl, text)
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

    print(f"fixed {total} markdown links")


if __name__ == "__main__":
    main()
