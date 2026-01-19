import subprocess
import sys
import os
import json

def read_file(file_path):
    """Read and return the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"

def run_python_file(file_path):
    """Run a Python script and capture its output."""
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error running file: {e}",
            "exit_code": -1
        }

def write_file(file_path, content):
    """Write content to a file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

def get_history_log_path(file_path):
    dir_name = os.path.dirname(file_path)
    # print("Directory name:", dir_name)
    base_name = os.path.basename(file_path)
    # print("Base name:", base_name)
    log_name = f"{base_name}_history_log.json"
    # print("Log name:", log_name)
    return os.path.join(dir_name, log_name)

def load_history_log(log_path):
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history_log(log_path, new_session):
    print(f"Saving history log to: {log_path}")
    try:
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except Exception:
                    history = []
        else:
            history = []
        history.append(new_session)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Failed to save history log: {e}")



