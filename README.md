# Advent of Code

## Editions

- 2015
- 2016
- 2017
- 2018
- 2019 [partial]
- 2020
- 2021 [completed]
- 2022 [completed]
- 2023 [completed]
- 2024 [completed]
- 2025 - TAPL [completed]

## TAPL Editions

Starting from 2025, [TAPL](https://github.com/HetorusNL/tapl) is used as programming language.
For now, the following should be performed to compile and run these years:

```bash
# clone the TAPL compiler repo in the tapl-lang/ folder in this repository (is in gitignore)
git clone git@github.com:HetorusNL/tapl-lang.git

# run the days like follows
uv run -m tapl-lang.src.compilers.compyler [year]/[day]/part[x].tim
# e.g.
uv run -m tapl-lang.src.compilers.compyler 2025/01/part1.tim

# or run all days of 2025 (with verifying the outputs) as follows
uv run run_all.py
```
