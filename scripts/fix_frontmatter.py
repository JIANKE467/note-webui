import argparse
import re
from pathlib import Path


URL_JSON_RE = re.compile(
    r"^[ \t\ufeff]*\"url\"\s*:\s*\"https?://[^\"]+\"\s*,?\s*$",
    re.IGNORECASE,
)
URL_YAML_RE = re.compile(
    r"^[ \t\ufeff]*url\s*:\s*https?://\S+\s*$",
    re.IGNORECASE,
)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.lstrip("\ufeff").startswith("---"):
        return 0
    lines = text.splitlines(keepends=True)
    if not lines:
        return 0
    if lines[0].lstrip("\ufeff").strip() != "---":
        return 0

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return 0

    front_lines = lines[: end_idx + 1]
    kept = []
    removed = 0
    for line in front_lines:
        stripped = line.rstrip("\r\n")
        if URL_JSON_RE.match(stripped) or URL_YAML_RE.match(stripped):
            removed += 1
            continue
        if "\"url\"" in stripped and "http" in stripped:
            removed += 1
            continue
        if stripped.lstrip().startswith("url:") and "http" in stripped:
            removed += 1
            continue
        kept.append(line)

    if removed:
        new_text = "".join(kept + lines[end_idx + 1 :])
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
    files = 0
    for path in root.rglob("*.md"):
        files += 1
        total += fix_file(path)

    print(f"fixed {total} front matter url fields")
    if total == 0:
        hits = []
        for path in root.rglob("*.md"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if "\"url\"" in text and "http" in text:
                hits.append(path.as_posix())
            if len(hits) >= 3:
                break
        if hits:
            print("sample files containing url fields:")
            for item in hits:
                print(f"- {item}")
        else:
            print(f"scanned {files} markdown files, no url fields found")


if __name__ == "__main__":
    main()
