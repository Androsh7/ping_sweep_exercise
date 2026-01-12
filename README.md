# Ping Sweep Exercise

This is an exercise to create a python program capable of pinging a range of hosts

## Setup

1. Fork the repository in Github
2. Clone the repository using your IDE, or run `git clone <FORKED REPO URL>` via the cli
3. Create a python virtual environment using your IDE, or by running `python3 -m venv .venv` within the repo directory
4. Switch to the newly created virtual environment `.venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Linux)
5. Install development tools using `pip install -e .[dev]`
6. Create a feature branch using `git switch -c feature/initial_function`
7. Start writing code
8. Once your code is complete create a PR (Pull Request) in Github to merge it into your main branch

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
This is a python linter, it goes through your code, finds errors, and gives you a final score. I recommend aiming for a score of 8-10 after all reasonable suggestions have been applied.

```
pylint . # Lint the whole repo
pylint main.py # Lint a specific file
```

## Customer requirements

Requirements:
- ~~Basic CLI interface, I.E: `python main.py --ping 192.168.1.1`~~ (This has already been done)
- Allow users to specify multiple IP addresses I.E: `"127.0.0.1,127.0.0.2,127.0.0.3"`
- Allow users to specify a range of IP addresses `172.16.0.0-172.16.1.1`
- Returns an accurate summary of which hosts are and aren't readable

Ideal (bonus):
- Allow users to specify a network to ping `172.16.1.1/24`
- Show an ETA (check out the tqdm library for this)
- Run pings simultaneously (multi-threading)

Restrictions:
- Cannot be a wrapper for an external application, I.E: nmap, masscan, etc

## Tips

1. Multiple libraries implement a mechanism for pinging a host, however the easiest is via the `ping` standard library which has a simple function to ping a host
2. Complex inputs like `127.0.0.1/24` can be difficult to parse all together, instead try breaking up the IP and CIDR into separate pieces, that can then be used to create a more machine readable format like `["127.0.0.1", "127.0.0.2", "127.0.0.3", ...]`
3. Avoid using CLI commands, I.E: `subprocess.run("ping -c 1")` while this can seemingly make your job easier, it requires significantly more work to parse the output, handle errors, and allow for OS cross-compatibility