from pathlib import Path
from app.config import settings

print(f"Base directory: {settings.BASE_DIR}")
print(f"Dataset path: {settings.DATASET_PATH}")
print(f"Dataset exists: {settings.DATASET_PATH.exists()}")
print(f"Is directory: {settings.DATASET_PATH.is_dir()}")

if settings.DATASET_PATH.exists():
    files = list(settings.DATASET_PATH.rglob("*"))
    print(f"Files found: {len(files)}")
    for f in files:
        if f.is_file():
            print(f"  - {f.name} ({f.stat().st_size / (1024*1024):.1f} MB)")