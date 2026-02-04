import os
import shutil

IMG_DIR = "img"
CATEGORY_IMG = "list_category_img.txt"
CATEGORY_CLOTH = "list_category_cloth.txt"
OUT_DIR = "aura_dataset"

# ===============================
# AURA v1 target mapping
# ===============================
TARGET = {
    "tshirt": ["tee"],
    "shirt": ["shirt", "button-down"],
}

# ===============================
# Step 1: category_id (line number) -> category_name
# ===============================
id_to_name = {}

with open(CATEGORY_CLOTH, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f, start=1):  # LINE NUMBER = category_id
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        name = parts[0].lower()
        id_to_name[idx] = name

# ===============================
# Step 2: create output folders
# ===============================
os.makedirs(OUT_DIR, exist_ok=True)
for cls in TARGET:
    os.makedirs(os.path.join(OUT_DIR, cls), exist_ok=True)

# ===============================
# Step 3: filter images
# ===============================
copied = 0
skipped = 0

with open(CATEGORY_IMG, "r", encoding="utf-8") as f:
    lines = f.readlines()[2:]  # ✅ skip first 2 lines

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) != 2:
            skipped += 1
            continue

        img_path, cid = parts
        cid = int(cid)

        if cid not in id_to_name:
            continue

        cname = id_to_name[cid]

        for aura_class, keywords in TARGET.items():
            if any(k in cname for k in keywords):
                src = img_path  # ✅ full relative path already correct
                dst = os.path.join(
                    OUT_DIR,
                    aura_class,
                    os.path.basename(img_path)
                )

                if os.path.exists(src):
                    shutil.copy(src, dst)
                    copied += 1
                else:
                    skipped += 1
                break

print(f"Done. Images copied: {copied}")
print(f"Skipped lines/files: {skipped}")
