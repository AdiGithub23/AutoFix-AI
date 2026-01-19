import os
import sys
import subprocess
from google import genai
from dotenv import load_dotenv

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

def append_to_file(file_path, content):
    try:
        with open(file_path, "a", encoding="utf-8") as f:  # Use "a" for append mode
            f.write(content)
        print("\nContent appended successfully!")
    except Exception as e:
        print(f"Error writing to file: {e}")


if __name__ == "__main__":
    file_path = r"F:\_Fast Drive (H)\A2Z-AI\13-AI_Agents_with_Pure_Python\AutoFix-AI\test_scripts\test_calculator.py"
    result = run_python_file(file_path)
    if not result:
        exit(1)
    
    terminal_output = (
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}\n"
        f"Exit Code: {result.returncode}\n"
    )

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
    prompt = (
        "Here is the terminal results of a Python script:\n\n"
        f"{terminal_output}\n\n"
        "In a few words, identify errors/ isssues in the output above"
        "Please answer in plain text, without any Markdown or LaTeX formatting."
    )

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    print("LLM Response:\n")
    print(response.text)

    content = f'\n\n\n{response.text}'
    append_to_file(file_path, content)
