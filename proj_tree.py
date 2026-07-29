from pathlib import Path

IGNORE_DIRS = {
    ".venv",
    ".git",
    ".idea",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache"
}

IGNORE_FILES = {
    ".DS_Store"
}


def print_tree(path: Path, prefix=""):
    entries = sorted(
        [e for e in path.iterdir()
         if e.name not in IGNORE_DIRS
         and e.name not in IGNORE_FILES],
        key=lambda e: (e.is_file(), e.name.lower())
    )

    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree(entry, prefix + extension)


print(Path(".").resolve().name)
print_tree(Path("."))