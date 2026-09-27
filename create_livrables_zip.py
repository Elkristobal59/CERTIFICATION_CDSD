import os
import zipfile
import shutil

ROOT_DIR = r"d:\PROJETS JEDHA\CERTIFICATION_CDSD"
OUT_DIR = os.path.join(ROOT_DIR, "LIVRABLES_ZIP")
os.makedirs(OUT_DIR, exist_ok=True)

BLOCKS = [
    ("Bloc_1_Kayak", "Livrables_Bloc_1_Kayak.zip"),
    ("Bloc_2_Analyse_Exploratoire", "Livrables_Bloc_2_Analyse_Exploratoire.zip"),
    ("Bloc_3_Machine_Learning", "Livrables_Bloc_3_Machine_Learning.zip"),
    ("Bloc_4_ATT_Spam_Detector", "Livrables_Bloc_4_ATT_Spam_Detector.zip"),
    ("Bloc_5_Getaround", "Livrables_Bloc_5_Getaround.zip"),
    ("Bloc_6_CliNER", "Livrables_Bloc_6_CliNER.zip"),
]

EXCLUDE_DIRS = {"__pycache__", ".ipynb_checkpoints", ".pytest_cache", ".ruff_cache", "mlruns", ".venv", "venv", "env", "node_modules"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".tmp"}
EXCLUDE_EXACT_FILES = {".env"}

def should_exclude(filename):
    f_lower = filename.lower()
    if filename in EXCLUDE_EXACT_FILES:
        return True
    if filename.startswith("~$"):
        return True
    ext = os.path.splitext(filename)[1].lower()
    if ext in EXCLUDE_EXTS:
        return True
    # Règle stricte jury : aucune fiche de révision, mémo ou guide personnel dans les livrables
    if "fiche_revision" in f_lower or "fiche_memo" in f_lower or "guide_soutenance" in f_lower or "aide_memoire" in f_lower:
        return True
    return False

def zip_folder(folder_path, output_zip):
    print(f"Creating {output_zip}...")
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if should_exclude(file):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, os.path.dirname(folder_path))
                zf.write(full_path, rel_path)
    sz_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f" -> {os.path.basename(output_zip)} ({sz_mb:.2f} MB)")

for block_dir, zip_name in BLOCKS:
    src_dir = os.path.join(ROOT_DIR, block_dir)
    dst_zip = os.path.join(OUT_DIR, zip_name)
    if os.path.exists(src_dir):
        zip_folder(src_dir, dst_zip)

print("\nAll 6 block zip archives generated successfully in LIVRABLES_ZIP (strictly jury deliverables)!")
