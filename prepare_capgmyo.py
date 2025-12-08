import os
import zipfile
import shutil
import glob

ROOT = r"C:\Users\SULEMAN KHAN\emgbench"
ZIP_NAME = "capg-dbb.zip"

zip_path = os.path.join(ROOT, ZIP_NAME)
if not os.path.exists(zip_path):
    raise FileNotFoundError(f"Could not find {zip_path}. Make sure capg-dbb.zip is in the emgbench folder.")

print(f"[1] Extracting {zip_path} ...")
with zipfile.ZipFile(zip_path, "r") as zf:
    zf.extractall(ROOT)

print("[2] Removing __MACOSX if it exists ...")
macosx_dir = os.path.join(ROOT, "__MACOSX")
if os.path.isdir(macosx_dir):
    shutil.rmtree(macosx_dir)

# Find the dbb folder (it might be directly under ROOT or inside capg-dbb)
dbb_dir = os.path.join(ROOT, "dbb")
if not os.path.isdir(dbb_dir):
    possible = os.path.join(ROOT, "capg-dbb", "dbb")
    if os.path.isdir(possible):
        print(f"[3] Moving {possible} -> {dbb_dir}")
        shutil.move(possible, dbb_dir)
        capg_root = os.path.join(ROOT, "capg-dbb")
        if os.path.isdir(capg_root):
            shutil.rmtree(capg_root)
    else:
        raise FileNotFoundError("Could not find a 'dbb' folder after unzipping. Please check the zip contents.")

print(f"[4] Preparing CapgMyo_B folder structure ...")
capg_dir = os.path.join(ROOT, "CapgMyo_B")
os.makedirs(capg_dir, exist_ok=True)

files = glob.glob(os.path.join(dbb_dir, "*"))
print(f"    Found {len(files)} files in dbb/")

for file_path in files:
    filename = os.path.basename(file_path)
    # Same logic as bash script:
    # aaa=$(echo "$filename" | cut -d'-' -f1 | cut -c1-3)
    prefix = filename.split("-")[0][:3]
    dest_dir = os.path.join(capg_dir, f"dbb-preprocessed-{prefix}")
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)
    print(f"    Moving {filename} -> {dest_dir}")
    shutil.move(file_path, dest_path)

print("[5] Removing original dbb folder ...")
shutil.rmtree(dbb_dir)

print("✅ Done preparing CapgMyo_B dataset structure.")
print(f"   Final dataset root: {capg_dir}")
