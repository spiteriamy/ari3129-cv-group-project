"""
Member Merger – CLI Tool

This script merges Label Studio annotation JSON files and image ZIP files
from multiple team members into a single merged dataset.

USAGE:
------
python member_merger_cli.py \
  --member "Alice Smith" alice.json alice_images.zip \
  --member "Bob Borg" bob.json bob_images.zip \
  --member "Cara Vella" cara.json cara_images.zip

REQUIREMENTS:
-------------
- Python 3.9 or newer
- JSON exports must be valid Label Studio task arrays
- ZIP files must contain the corresponding annotated images

OUTPUT:
-------
- Merger/merged_input.json
- Merger/merged_images.zip
"""
import argparse
import json
import shutil
import zipfile
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Tuple

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

# ---- Helpers ----

def safe_name(s: str) -> str:
    return "".join(ch if ch.isalnum() or ch in (" ", "_", "-", ".") else "_" for ch in s.strip())

def load_ls_array(p: Path) -> List[Dict[str, Any]]:
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{p} is not a Label Studio task array.")
    return data

def task_key(task: Dict[str, Any]) -> str:
    fu = task.get("file_upload")
    if fu:
        return str(fu)
    img = (task.get("data") or {}).get("image", "")
    return Path(img).name or str(img)

def merge_ls_tasks(task_lists: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    bucket = defaultdict(list)
    for tl in task_lists:
        for t in tl:
            bucket[task_key(t)].append(t)

    merged = []
    for _, tasks in bucket.items():
        tasks_sorted = sorted(tasks, key=lambda t: len(t.get("annotations", [])), reverse=True)
        base = json.loads(json.dumps(tasks_sorted[0]))

        all_anns = []
        for t in tasks:
            all_anns.extend(t.get("annotations", []) or [])

        new_anns = []
        next_id = 1
        for ann in all_anns:
            ann_copy = json.loads(json.dumps(ann))
            ann_copy["id"] = next_id
            next_id += 1
            for r in ann_copy.get("result", []) or []:
                r["id"] = r.get("id") or f"res_{ann_copy['id']}_{hashlib.md5(str(r).encode()).hexdigest()[:6]}"
            new_anns.append(ann_copy)

        base["annotations"] = new_anns
        merged.append(base)

    return merged

def sha1_of_file(p: Path, buf_size: int = 1 << 20) -> str:
    h = hashlib.sha1()
    with p.open("rb") as f:
        while True:
            b = f.read(buf_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def extract_and_flatten_zips(zip_paths: List[Path], dest_dir: Path) -> Tuple[int, int]:
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    seen_hash = {}
    written = skipped = 0
    tmp_root = dest_dir.parent / "_unzips_tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)

    try:
        for zp in zip_paths:
            with zipfile.ZipFile(zp, "r") as zf:
                zf.extractall(tmp_root)

        for p in tmp_root.rglob("*"):
            if not p.is_file():
                continue
            if p.name.startswith("._") or "DS_Store" in p.name:
                continue
            if p.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            sha1 = sha1_of_file(p)
            if sha1 in seen_hash:
                skipped += 1
                continue

            dst = dest_dir / p.name
            if dst.exists():
                dst = dest_dir / f"{p.stem}_{sha1[:8]}{p.suffix}"

            shutil.copy2(p, dst)
            seen_hash[sha1] = dst.name
            written += 1
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    return written, skipped

def zip_dir(src_dir: Path, out_zip: Path):
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(src_dir.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(src_dir))

# ---- CLI ----

def main():
    parser = argparse.ArgumentParser(
        description="Merge Label Studio annotations and image ZIPs from multiple team members."
    )
    parser.add_argument(
        "--member",
        action="append",
        nargs=3,
        metavar=("NAME", "JSON", "ZIP"),
        required=True,
        help="Member entry: FULL_NAME annotations.json images.zip"
    )
    parser.add_argument("--out-dir", default="Merger", help="Output directory")
    args = parser.parse_args()

    if not (2 <= len(args.member) <= 4):
        raise RuntimeError("Team size must be between 2 and 4 members.")

    root = Path.cwd()
    merger_dir = root / args.out_dir
    indiv_dir = merger_dir / "Individuals"
    img_work = merger_dir / "Temp"

    for d in (merger_dir, indiv_dir, img_work):
        d.mkdir(parents=True, exist_ok=True)

    task_lists = []
    zip_paths = []

    for name, json_path, zip_path in args.member:
        safe = safe_name(name).replace(" ", "_")
        jp = Path(json_path)
        zp = Path(zip_path)

        if not jp.exists():
            raise FileNotFoundError(jp)
        if not zp.exists():
            raise FileNotFoundError(zp)

        shutil.copy2(jp, indiv_dir / f"input_{safe}.json")
        shutil.copy2(zp, indiv_dir / f"images_{safe}.zip")

        task_lists.append(load_ls_array(jp))
        zip_paths.append(zp)

    merged_tasks = merge_ls_tasks(task_lists)
    merged_json = merger_dir / "merged_input.json"
    with merged_json.open("w", encoding="utf-8") as f:
        json.dump(merged_tasks, f, ensure_ascii=False, indent=2)

    written, skipped = extract_and_flatten_zips(zip_paths, img_work)
    merged_zip = merger_dir / "merged_images.zip"
    zip_dir(img_work, merged_zip)

    shutil.rmtree(img_work, ignore_errors=True)

    print("Merge complete.")
    print(f"Merged JSON: {merged_json}")
    print(f"Merged images ZIP: {merged_zip}")
    print(f"Images written: {written} | Duplicates skipped: {skipped}")
    print(f"Merged tasks: {len(merged_tasks)}")

if __name__ == "__main__":
    main()
