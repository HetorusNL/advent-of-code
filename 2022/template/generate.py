from pathlib import Path
import shutil

# constants
NUMBER_OF_DAYS: int = 25


def main():
    """generate or update the days that have not been solved with the template code"""
    # formulate the path to the root of this years solutions folder and the template folder
    this_year_folder = (Path(__file__).parent / "..").resolve()
    template_folder = this_year_folder / "template" / "template_files"

    # loop through the days and generate the template
    for day in range(1, NUMBER_OF_DAYS + 1):
        day_folder = this_year_folder / f"{day:>02}"
        # check if the directory already exists
        if day_folder.is_dir():
            # check if it contains input files
            input_files = list(filter(lambda file: file.name.endswith(".txt"), (day_folder / "input_files").iterdir()))
            if len(input_files) != 0:
                # skip this day, as it already has input files, thus we assume modifications/solutions
                continue
        # if we end up here, this day folder can be generated
        # so copy everything from template_files/ to the day_folder
        print(f"generating template to folder: {day_folder}")
        shutil.rmtree(day_folder)
        shutil.copytree(template_folder, day_folder, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
