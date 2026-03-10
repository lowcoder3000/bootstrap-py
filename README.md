
## What Is This

Python Bootstrapper is a lightweight, cross-platform launcher module that ensures your Python scripts run in a controlled, isolated environment. It handles the creation and management of a virtual environment (venv), installs dependencies automatically, and applies environment configurations from `.env` files and optional shell scripts.

This module is intended to simplify development workflows, streamline onboarding, and eliminate common runtime issues related to missing virtual environments or dependencies.

## Features

- Automatically creates and activates a venv/ directory if not present
- Installs Python packages from requirements.txt (only when changes are detected)
- Loads environment variables from a .env file
- Relaunches the original script within the virtual environment context
- Fully cross-platform: Windows, macOS, Linux
- Requires no external packages or dependencies

## Installation

1. Copy `bootstrap.py` into your project directory.
2. Import and call it at the start of any Python script you want to bootstrap.

## Example Directory Structure

```
my_project/
├── bootstrap.py           # The reusable venv manager
├── example.py             # Example script using bootstrap
├── requirements.txt       # Optional dependency list
├── .env                   # Optional environment variables

└── venv/                  # Created automatically
```

## Usage

1. Add `bootstrap.py` to your project

```
curl -O https://raw.githubusercontent.com/lowcoder3000/bootstrap-py/main/bootstrap.py
```

This file can be reused across multiple Python entry points in the same project.

2. Use it in any script

Example (example.py):

```
import bootstrap
bootstrap.ensure_venv()

# Your script logic here
print("Application is running inside virtualenv.")
```

3. Define your dependencies

Create a `requirements.txt` file in the root of your project:

4. (Optional) Add a `.env` file

Variables will be loaded into os.environ, example:

```
API_KEY=your-api-key  
DEBUG=true
```
You probably want to add this file to your `.gitignore`.



## Behavior Overview

When a script is run, the bootstrapper performs the following:

1. Checks if the script is already running inside a virtual environment.
2. If not:
   - Creates the virtual environment in the `venv/` folder using the system Python interpreter.
   - Installs or reinstalls packages listed in `requirements.txt` only if the file has changed (tracked using a hash stored in the venv folder).
    - Loads environment variables from `.env`.
   - Relaunches the same script inside the new environment.
3. If already inside a virtual environment:
   - Loads `.env` directly and proceeds with execution.

## Why Use This

- Ensures consistent, reliable execution environments
- Avoids missing package issues and setup inconsistencies
- Simplifies onboarding for developers and team members
- Ideal for internal tools, CLI utilities, and reproducible script-based workflows

## License

This project is licensed under the MIT License.

## Acknowledgements

Inspired by tools like `npx`, `pipx`, and patterns used in monorepo development workflows.
