"""
scripts/package_release.py - Create a clean release zip for TW Quant Cockpit.

Usage:
    python scripts/package_release.py

Output:
    dist/tw_quant_cockpit_v0.2_phase4.zip

Excludes:
    .git/ .claude/ __pycache__/ *.pyc *.pyo *.db *.sqlite *.sqlite3
    .env data/reports/ saved_models/ data_cache/ reports_output/ logs/ *.zip

Includes:
    All source code, README.md, requirements.txt, .env.example,
    config/, data/import/*_sample.csv
"""

import os
import sys
import zipfile

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_EXCLUDE_DIRS = {
    '.git', '.claude', '__pycache__', 'data_cache',
    'reports_output', 'logs', 'saved_models',
}

_EXCLUDE_DIR_PATHS = [
    os.path.join('data', 'reports'),
]

_EXCLUDE_EXTENSIONS = {'.pyc', '.pyo', '.db', '.sqlite', '.sqlite3', '.zip'}

_EXCLUDE_FILES = {'.env'}

_OUTPUT_DIR = os.path.join(_PROJECT_ROOT, 'dist')
_OUTPUT_ZIP = os.path.join(_OUTPUT_DIR, 'tw_quant_cockpit_v0.2_phase4.zip')


def _should_exclude(rel_path: str) -> bool:
    """Return True if this relative path should be excluded from the zip."""
    parts = rel_path.replace('\\', '/').split('/')

    # Exclude hidden / cache directories
    for part in parts[:-1]:  # directory parts only
        if part in _EXCLUDE_DIRS:
            return True

    # Exclude specific directory paths (like data/reports/)
    for excl in _EXCLUDE_DIR_PATHS:
        excl_norm = excl.replace('\\', '/').rstrip('/')
        path_norm = rel_path.replace('\\', '/').rstrip('/')
        if path_norm == excl_norm or path_norm.startswith(excl_norm + '/'):
            return True

    # Filename checks
    fname = parts[-1]

    if fname in _EXCLUDE_FILES:
        return True

    _, ext = os.path.splitext(fname)
    if ext.lower() in _EXCLUDE_EXTENSIONS:
        return True

    # Exclude non-sample CSVs inside data/import/ that are standard output files
    # (keep *_sample.csv, exclude the generated standard CSVs from the package)
    if 'data/import/' in rel_path.replace('\\', '/'):
        if fname.endswith('.csv') and not fname.endswith('_sample.csv'):
            return True

    return False


def build_zip():
    os.makedirs(_OUTPUT_DIR, exist_ok=True)

    included = 0
    excluded = 0

    with zipfile.ZipFile(_OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(_PROJECT_ROOT):
            # Prune excluded directories in-place so os.walk skips them
            dirnames[:] = [
                d for d in dirnames
                if d not in _EXCLUDE_DIRS
            ]

            for filename in filenames:
                abs_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(abs_path, _PROJECT_ROOT)

                if _should_exclude(rel_path):
                    excluded += 1
                    continue

                zf.write(abs_path, rel_path)
                included += 1

    size_kb = os.path.getsize(_OUTPUT_ZIP) / 1024
    print(f"打包完成：{_OUTPUT_ZIP}")
    print(f"包含 {included} 個檔案，排除 {excluded} 個檔案")
    print(f"檔案大小：{size_kb:.1f} KB")


if __name__ == '__main__':
    print(f"專案目錄：{_PROJECT_ROOT}")
    print(f"輸出：{_OUTPUT_ZIP}")
    print()
    build_zip()
