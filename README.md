# Fitness Tracker (OOP)

![CI](https://github.com/vRUZIx/Fitness-Tracker-OOP/actions/workflows/ci.yml/badge.svg)

Small object-oriented fitness tracker example project.

## Project structure

- `src/` — application source code
- `tests/` — pytest test suite
- `data.json` — persistent data file (project root)

## Requirements

Install the test runner (used only for running tests):

```powershell
pip install -r requirements.txt
```

> `requirements.txt` currently contains `pytest` for running tests.

## Run the app

From the project root run:

```powershell
python src/main.py
```

This prints sample output and writes to `data.json` at project root.

## Run tests

From the project root run:

```powershell
python -m pytest -q
```

## Notes and next steps

- `Repository` writes to `data.json` at the project root to avoid creating multiple files when running from different CWDs.
- You can extend models, add CLI options to `src/main.py`, or add CI (GitHub Actions) for automated tests.
