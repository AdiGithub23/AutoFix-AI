import os
import json
from dotenv import load_dotenv
from google import genai
from src.agent.agent_functions import read_file, run_python_file

def call_llm(prompt):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )
    return response.text

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

def process_file(file_path, max_attempts=2):
    log_path = get_history_log_path(file_path)
    session_history = load_history_log(log_path)

    history = []
    for attempt in range(1, max_attempts + 1):
        file_content = read_file(file_path)
        if file_content is None:
            return {
                "error": f"Could not read file: {file_path}",
                "history": history
            }
        run_result = run_python_file(file_path)
        prompt = (
            f"Attempt {attempt}:\n"
            "Here is a Python script:\n"
            "---\n"
            f"{file_content}\n"
            "---\n"
            "Here is its output:\n"
            f"STDOUT:\n{run_result['stdout']}\n"
            "---\n"
            f"STDERR:\n{run_result['stderr']}\n"
            f"Exit Code: {run_result['exit_code']}\n\n"
            "If there are any syntax errors, issues, or problems in the code or output, "
            "fix the code and return ONLY the corrected code. "
            "Add a comment wherever an update is made. "
            "If there are no issues, return the original code."
        )

        llm_response = call_llm(prompt)
        if llm_response is None:
            return {
                "error": "LLM did not return a response.",
                "history": history
            }
        fixed = llm_response.strip() != file_content.strip()
        attempt_record = {
            "attempt": attempt,
            "file_content": file_content,
            "run_result": run_result,
            "llm_prompt": prompt,
            "llm_response": llm_response,
            "file_fixed": fixed
        }
        history.append(attempt_record)

        if fixed:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(llm_response)
        else:
            break

    session_history.append({
        "file_path": file_path,
        "session_history": history
    })
    
    save_history_log(log_path, {
        "file_path": file_path,
        "session_history": history
    })

    return {
        "history": history,
        "final_status": "success" if not history[-1]["file_fixed"] else "max_attempts_reached"
    }

