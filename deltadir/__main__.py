#!/usr/bin/env python3
import argparse
import os
import shutil
import hashlib
from datetime import datetime

def hash_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def compare_files(src_file, dst_file, method="existence"):
    if not os.path.exists(dst_file):
        return True, "missing"
    if method == "existence":
        return False, ""
    elif method == "mtime":
        src_mtime = os.path.getmtime(src_file)
        dst_mtime = os.path.getmtime(dst_file)
        if src_mtime != dst_mtime:
            return True, f"mtime differs: src={datetime.fromtimestamp(src_mtime)} dst={datetime.fromtimestamp(dst_mtime)}"
    elif method == "size":
        src_size = os.path.getsize(src_file)
        dst_size = os.path.getsize(dst_file)
        if src_size != dst_size:
            return True, f"size differs: src={src_size} dst={dst_size}"
    elif method == "hash":
        src_hash = hash_file(src_file)
        dst_hash = hash_file(dst_file)
        if src_hash != dst_hash:
            return True, f"hash differs: src={src_hash[:8]} dst={dst_hash[:8]}"
    return False, ""

def main():
    parser = argparse.ArgumentParser(description="Compare directories and perform actions on differences.")
    parser.add_argument("src", help="Source directory")
    parser.add_argument("dst", help="Destination directory")
    parser.add_argument("-m", "--method", choices=["existence", "mtime", "size", "hash"], default="existence",
                        help="Comparison method (default: existence)")
    parser.add_argument("-a", "--action", choices=["report", "copy"], default="copy",
                        help="Action to perform on differences (default: copy)")
    parser.add_argument("--overwrite", action="store_true",
                        help="If set, overwrite files when copying")
    args = parser.parse_args()

    for root, _, files in os.walk(args.src):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, args.src)
            dst_file = os.path.join(args.dst, rel_path)

            is_diff, reason = compare_files(src_file, dst_file, args.method)
            if is_diff:
                print(f"DIFF: {rel_path} -> {reason}")
                if args.action == "copy":
                    if not os.path.exists(dst_file) or args.overwrite:
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        print(f"COPY: {rel_path}")

if __name__ == "__main__":
    main()
