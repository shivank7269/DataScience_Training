import zipfile
import os
import shutil
from pathlib import Path
import random

# Step 1: Already done ✅
print("🔄 Step 1: Using existing extraction...")

# Step 2: Create target structure
base_dir = Path("weekly_practicle_project_14march]/dataset")  # New clean folder
for split in ['train', 'validation']:
    for category in ['recyclable', 'organic', 'non_recyclable']:
        (base_dir / split / category).mkdir(parents=True, exist_ok=True)

# Step 3: UNIVERSAL folder detection + mapping
print("\n🔍 Step 3: Auto-detecting folders...")
extract_dir = "dataset"  # Your extracted path

all_images = {'recyclable': [], 'organic': [], 'non_recyclable': []}

# Walk through ALL subfolders and classify
for root, dirs, files in os.walk(extract_dir):
    folder_name = Path(root).name.lower()

    # Smart classification based on folder names
    if any(word in folder_name for word in ['cardboard', 'glass', 'metal', 'plastic']):
        category = 'recyclable'
    elif any(word in folder_name for word in ['trash', 'misc', 'battery', 'textile']):
        category = 'non_recyclable'
    elif any(word in folder_name for word in ['paper']):
        category = 'organic'
    else:
        continue  # Skip unknown folders

    # Collect images
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            all_images[category].append(os.path.join(root, file))

print("📊 Found images:")
for cat, imgs in all_images.items():
    print(f"  {cat}: {len(imgs)} images")

# Step 4: 80/20 split
print("\n🔄 Step 4: 80/20 split...")
for category, images in all_images.items():
    if images:
        random.shuffle(images)
        train_end = int(0.8 * len(images))

        # Train split
        for src in images[:train_end]:
            filename = Path(src).name
            dst = base_dir / 'train' / category / filename
            if not dst.exists():
                shutil.copy2(src, dst)

        # Validation split
        for src in images[train_end:]:
            filename = Path(src).name
            dst = base_dir / 'validation' / category / filename
            if not dst.exists():
                shutil.copy2(src, dst)

# Step 5: Final count (TASK 1)
print("\n" + "=" * 60)
print("📈 TASK 1 DELIVERABLE - FINAL STRUCTURE")
print("=" * 60)
for split in ['train', 'validation']:
    print(f"\n{split.upper()}:")
    total = 0
    for cat in ['recyclable', 'organic', 'non_recyclable']:
        path = base_dir / split / cat
        count = len([f for f in path.iterdir() if f.suffix.lower() in ['.jpg', '.png']])
        print(f"  {cat}: {count:3d} images")
        total += count
    print(f"  Total: {total:3d} images")
