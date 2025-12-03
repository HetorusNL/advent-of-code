import subprocess
from pathlib import Path
from time import time_ns


YEAR: str = "2025"


def run_part(day: str, part: int) -> None:
    start: int = time_ns()
    result = subprocess.run(
        f"uv run -m tapl.src.compilers.compyler {YEAR}/{day}/part{part}.tim",
        shell=True,
        capture_output=True,
        text=True,
    )
    duration: int = time_ns() - start
    lines = result.stdout.strip().split("\n")
    for line in lines:
        if line.startswith("[solution]"):
            time: str = f"{(int(duration//1e9))}.{int((duration//1e6)%1e3):03d}s"
            print(f"Day {day} Part {part}: [{time}] {line}")


# Find all day folders in 2025 directory
year_path = Path(YEAR)
day_folders = sorted([d for d in year_path.iterdir() if d.is_dir() and d.name.isdigit()])

for day_folder in day_folders:
    day: str = day_folder.name
    run_part(day, 1)
    run_part(day, 2)
