import argparse
from pathlib import Path


def has_child_markdown(dir_path: Path) -> bool:
    for child in dir_path.iterdir():
        if child.is_dir():
            if any(p.suffix.lower() == ".md" for p in child.rglob("*.md")):
                return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="data root directory")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"root not found: {root}")

    renamed = 0
    for dir_path in root.rglob("*"):
        if not dir_path.is_dir():
            continue
        index_md = dir_path / "index.md"
        if not index_md.exists():
            continue
        if (dir_path / "_index.md").exists():
            continue
        if not has_child_markdown(dir_path):
            continue
        index_md.rename(dir_path / "_index.md")
        renamed += 1

    print(f"renamed {renamed} index.md to _index.md")


if __name__ == "__main__":
    main()
