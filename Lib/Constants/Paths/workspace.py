from pathlib import Path


def findDirectory(directory: str = "workspace") -> Path:
    start_path = Path(__file__).resolve()
    anchor = f".{directory}"

    for parent in [start_path.parent] + list(start_path.parents):
        if (parent / anchor).exists():
            return parent

    raise FileNotFoundError("Ensure the marker-file '.workspace' exists.")


WORKSPACE = findDirectory()
