import csv
from pathlib import Path


def prepare_file(path):
    file_path = Path(path)
    file_path.write_text("", encoding="utf-8")
    return file_path


def save_to_csv(path, rows):
    fieldnames = ["title", "company", "link", "salary", "city"]
    file_path = Path(path)
    with file_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def clean_text(value):
    if not value:
        return ""
    return " ".join(value.split())
