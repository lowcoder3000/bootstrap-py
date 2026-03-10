# https://github.com/https://github.com/lowcoder3000/bootstrap.py

import os
import sys
import subprocess
import venv as venv_mod
import hashlib

DEBUG = os.environ.get("DEBUG") == "1"

def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def in_venv():
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )

def get_paths():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    venv_dir = os.path.join(base_dir, "venv")

    env_file = os.path.join(base_dir, ".env")
    requirements = os.path.join(base_dir, "requirements.txt")
    req_hash_path = os.path.join(venv_dir, ".requirements.hash")

    if os.name == "nt":
        python_bin = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_bin = os.path.join(venv_dir, "bin", "python")

    return base_dir, venv_dir, python_bin, env_file, requirements, req_hash_path

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def needs_install(requirements, req_hash_path):
    if not os.path.exists(requirements):
        return False
    if not os.path.exists(req_hash_path):
        return True
    with open(req_hash_path, "r") as f:
        stored_hash = f.read().strip()
    return hash_file(requirements) != stored_hash

def save_requirements_hash(requirements, req_hash_path):
    h = hash_file(requirements)
    with open(req_hash_path, "w") as f:
        f.write(h)

def create_venv_if_needed(venv_dir):
    if not os.path.exists(venv_dir):
        print(color(f"🔧 Creating virtual environment at: {venv_dir}", "34"))
        venv_mod.create(venv_dir, with_pip=True)

def install_requirements_if_needed(python_bin, requirements, req_hash_path):
    if needs_install(requirements, req_hash_path):
        print(color(f"📦 Installing requirements from {requirements}", "32"))
        cmd = [python_bin, "-m", "pip", "install", "-r", requirements]
        if DEBUG:
            print(color(f"DEBUG: {' '.join(cmd)}", "33"))
        subprocess.check_call(cmd)
        save_requirements_hash(requirements, req_hash_path)

def load_dotenv(env_file):
    # check global flag env already loaded
    if os.environ.get('ENV_LOADED'):
        return
    os.environ['ENV_LOADED'] = '1'  # Set flag to indicate .env has been loaded
    if os.path.exists(env_file):
        if DEBUG:
            print(color(f"DEBUG: Loading .env from {env_file}", "35"))
        with open(env_file) as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, val = line.strip().split("=", 1)
                    os.environ.setdefault(key, val)

def relaunch(script_path, script_args):
    _, venv_dir, venv_python, env_file, requirements, req_hash_path = get_paths()

    create_venv_if_needed(venv_dir)
    install_requirements_if_needed(venv_python, requirements, req_hash_path)
    load_dotenv(env_file)

    args = ' '.join(f'"{a}"' for a in [script_path] + script_args)
    try:
        cmd = f'{venv_python} {args}'
        if DEBUG:
            print(color(f"DEBUG: {cmd}", "33"))
        if os.name == "nt":
            subprocess.run(cmd, shell=True)
        else:
            subprocess.run(cmd, shell=True, executable="/bin/bash")
    except KeyboardInterrupt:
        print(color("\n✋ Interrupted.", "31"))
        sys.exit(130)
    except KeyboardInterrupt:
        print(color("\n👋 Interrupted.", "31"))
        sys.exit(130)
    sys.exit()

def ensure_venv(script_path=None, script_args=None):
    if in_venv():
        load_dotenv(get_paths()[4])
        return
    if script_path is None:
        script_path = os.path.abspath(sys.argv[0])
    if script_args is None:
        script_args = sys.argv[1:]
    relaunch(script_path, script_args)
