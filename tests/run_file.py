import subprocess
import sys
import os

def run_python_file(file_path):
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        print("=== STDOUT ===")
        print(result.stdout)
        print("=== STDERR ===")
        print(result.stderr)
        print(f"Exit Code: {result.returncode}")
        return result
    except Exception as e:
        print(f"Error running file: {e}")
        return None

if __name__ == "__main__":
    file_path = r"F:\_Fast Drive (H)\A2Z-AI\13-AI_Agents_with_Pure_Python\AutoFix-AI\test_scripts\test_calculator.py"
    run_python_file(file_path)