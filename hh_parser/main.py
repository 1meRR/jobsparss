from config import OUTPUT_FILE
from parser import filter_rows, parse_jobs, prepare_rows
from utils import save_to_csv


def run():
    rows = parse_jobs()
    filtered = filter_rows(rows)
    prepared = prepare_rows(filtered)
    if not prepared:
        return
    save_to_csv(OUTPUT_FILE, prepared)


if __name__ == "__main__":
    run()
