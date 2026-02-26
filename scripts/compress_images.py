import argparse
import os
from pathlib import Path

from PIL import Image


def iter_images(root: Path):
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    for path in root.rglob("*"):
        if path.suffix.lower() in exts and path.is_file():
            yield path


def compress_image(path: Path, max_dim: int, jpeg_quality: int):
    try:
        with Image.open(path) as img:
            img_format = img.format
            width, height = img.size
            scale = min(1.0, max_dim / max(width, height))
            if scale < 1.0:
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.LANCZOS)

            save_kwargs = {}
            if img_format in {"JPEG", "JPG", "WEBP"}:
                save_kwargs.update(
                    {
                        "quality": jpeg_quality,
                        "optimize": True,
                        "progressive": True,
                    }
                )
            elif img_format == "PNG":
                save_kwargs.update({"optimize": True})

            img.save(path, **save_kwargs)
    except Exception:
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="data root directory")
    parser.add_argument("--max-dim", type=int, default=2000)
    parser.add_argument("--jpeg-quality", type=int, default=82)
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"root not found: {root}")

    compressed = 0
    for path in iter_images(root):
        if compress_image(path, args.max_dim, args.jpeg_quality):
            compressed += 1

    print(f"compressed {compressed} images")


if __name__ == "__main__":
    main()
