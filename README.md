# Ping Sweep Exercise

This is an exercise to create a python program capable of pinging a range of hosts

## Setup

1. Fork the repository in Github
2. Clone the repository using your IDE, or run `git clone <FORKED REPO URL>` via the cli
3. Create a python virtual environment using your IDE, or by running `python3 -m venv .venv` within the repo directory
4. Switch to the newly created virtual environment `.venv/Scripts/Activate.ps1` (Windows) or `source .venv/bin/activate` (Linux)
5. Install development tools using `pip install -e .[dev]`
6. Create a feature branch using `git switch -c feature/initial_function`
7. Start writing code, ensuring you meet the [customer requirements](REQUIREMENTS.md)
8. Once your code is complete create a PR (Pull Request) in Github to merge into the main branch

## Dev Utilities

### Black

This is a commandline utility that automatically formats your python code

```
black . # Format whole repo
black main.py # Format a specific file
```

### Isort

This organizes all of your imports in alphabetical order

```
isort . # Format whole repo
isort main.py # Format a specific file
```

### Pylint

This is a python linter, it goes through your code, finds errors, and gives you a final score. NOTE: some suggestions are unreasonable to fully implement, once you get to a score of 8-10 use your discretion for what should be fixed.

```
pylint . # Lint the whole repo
pylint main.py # Lint a specific file
```

## Tips

1. Multiple libraries implement a mechanism for pinging a host, the `socket` library provides access to low-level socket operations, alternatively the `subprocess` library allows you to run cli commands directly at the cost of OS cross-compatibility, third-party libraries also exist with various draw-backs
2. Complex inputs like `127.0.0.1/24` can be difficult to parse all together, instead try breaking up the IP and CIDR into separate pieces, that can then be used to create a more machine readable format like `["127.0.0.1", "127.0.0.2", "127.0.0.3", ...]`
3. Try not to use any AI generated code, while AI can augment your coding, simply copy-pasting code creates massive tech debt in the form of code that is hard to debug and hard to improve
