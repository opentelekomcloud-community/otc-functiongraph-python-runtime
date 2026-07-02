#!/usr/bin/env python3
#######################################################################
# Create zip file for function code and dependencies
# - create dependencies if requirements.txt changed
# - create zip file with code from src and dependencies
#
# Output will be written to dist folder.
# Default output zip filename is code.zip,
# can be changed with -o option
#
# The zip file will have the following structure:
# .
# ├── src
# │   ├── FILE1.py
# │   └── ...
# ├── bootstrap (optional)
# ├── README.md (optional)
# ├── LICENSE (optional)
# └── <installed packages from requirements.txt> 
#
#######################################################################

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


#ROOT = Path(__file__).resolve().parent
ROOT = Path(os.getcwd())

DIST_DIR = ROOT / "dist"
DEPENDENCIES_DIR = DIST_DIR / "dependencies"
VENV_DIR = DIST_DIR / ".venv_dest"
REQUIREMENTS_FILE = ROOT / "requirements.txt"
REQUIREMENTS_HASH_FILE = DIST_DIR / ".requirements_hash"
DEFAULT_CODE_ZIP_NAME = "code.zip"
OPTIONAL_FILES = ("README.md", "LICENSE", "bootstrap")


def sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def hash_directory(path: Path) -> str:
    hasher = hashlib.sha1()
    for file_path in sorted(path.rglob("*")):
        if file_path.is_dir():
            continue
        if "__pycache__" in file_path.parts:
            continue
        if any(part.endswith(".egg-info") for part in file_path.parts):
            continue
        if "build" in file_path.parts or "dist" in file_path.parts:
            continue
        relative = file_path.relative_to(path).as_posix()
        hasher.update(relative.encode("utf-8"))
        hasher.update(file_path.read_bytes())
    return hasher.hexdigest()


def requirements_fingerprint() -> str:
    hasher = hashlib.sha1()
    content = REQUIREMENTS_FILE.read_text(encoding="utf-8")
    hasher.update(content.encode("utf-8"))

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            # Skip pip options such as -r, -c, --extra-index-url.
            continue

        local_path = (ROOT / line).resolve()
        if local_path.exists() and local_path.is_dir():
            hasher.update(str(local_path).encode("utf-8"))
            hasher.update(hash_directory(local_path).encode("utf-8"))

    return hasher.hexdigest()


def requirements_changed(new_hash: str) -> bool:
    if not REQUIREMENTS_HASH_FILE.exists():
        return True
    return REQUIREMENTS_HASH_FILE.read_text(encoding="utf-8").strip() != new_hash


def install_dependencies() -> None:
    shutil.rmtree(VENV_DIR, ignore_errors=True)
    shutil.rmtree(DEPENDENCIES_DIR, ignore_errors=True)

    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True, cwd=ROOT)

    venv_python = VENV_DIR / "bin" / "python3"
    subprocess.run(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "-U",
            "pip",
            "setuptools",
            "wheel",
        ],
        check=True,
        cwd=ROOT,
    )
    subprocess.run(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "-U",
            "--use-pep517",
            "-r",            
            str(REQUIREMENTS_FILE),
            "--target",
            str(DEPENDENCIES_DIR),
        ],
        check=True,
        cwd=ROOT,
    )


def add_tree(zip_file: ZipFile, base_dir: Path, arc_prefix: str = "") -> None:
    for path in sorted(base_dir.rglob("*")):
        if path.is_dir() or "__pycache__" in path.parts:
            continue
        relative_path = path.relative_to(base_dir)
        archive_path = Path(arc_prefix) / relative_path if arc_prefix else relative_path
        zip_file.write(path, archive_path.as_posix())


def build_package(output_filename: str = DEFAULT_CODE_ZIP_NAME) -> None:
    DIST_DIR.mkdir(exist_ok=True)
    code_zip = DIST_DIR / output_filename

    new_hash = requirements_fingerprint()
    if requirements_changed(new_hash):
        print("Changes detected in requirements.txt, packaging dependencies.")
        install_dependencies()
        REQUIREMENTS_HASH_FILE.write_text(new_hash, encoding="utf-8")
    else:
        print("No changes in requirements.txt, skipping venv creation.")

    with ZipFile(code_zip, "w", compression=ZIP_DEFLATED) as zip_file:
        add_tree(zip_file, ROOT / "src", "src")
        if DEPENDENCIES_DIR.exists():
            add_tree(zip_file, DEPENDENCIES_DIR)

        for name in OPTIONAL_FILES:
            path = ROOT / name
            if path.is_file():
                zip_file.write(path, name)

    print(f"Packaged code and dependencies into {code_zip.relative_to(ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package function source and dependencies into a zip archive."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_CODE_ZIP_NAME,
        help="Output zip filename under dist/ (default: code.zip)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build_package(args.output)