import os
from dotenv import load_dotenv
from google import genai
from src.agent.agent_functions import read_file, run_python_file, write_file, get_history_log_path, load_history_log, save_history_log

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

def get_last_session_status(session_history):
    if not session_history:
        return None
    last_session = session_history[-1]
    attempts = last_session.get("session_history", [])
    if not attempts:
        return None
    last_attempt = attempts[-1]
    return {
        "file_fixed": last_attempt.get("file_fixed", False),
        "run_result": last_attempt.get("run_result", {}),
        "llm_response": last_attempt.get("llm_response", ""),
        "attempts_count": len(attempts)
    }


def process_file(file_path, max_attempts=2):
    log_path = get_history_log_path(file_path)
    session_history = load_history_log(log_path)

    last_status = get_last_session_status(session_history)
    if last_status and not last_status["file_fixed"] and last_status["attempts_count"] >= max_attempts:
        return {
            "skipped": True,
            "reason": "Previous session reached max attempts and did not fix the file. Skipping further attempts.",
            "last_status": last_status
        }

    repeated_error = None
    if session_history and len(session_history) > 1:
        prev_errors = [
            s["session_history"][-1]["run_result"]["stderr"]
            for s in session_history
            if s["session_history"] and "stderr" in s["session_history"][-1]["run_result"]
        ]
        if len(prev_errors) >= 2 and prev_errors[-1] and prev_errors[-1] == prev_errors[-2]:
            repeated_error = prev_errors[-1]

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
        
        if repeated_error:
            prompt += (
                f"\n\nNote: The following error has occurred repeatedly in previous attempts:\n{repeated_error}\n"
                "Please try a different approach to fix this recurring issue."
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
            write_file(file_path, llm_response)
        else:
            break

    # session_history.append({
    #     "file_path": file_path,
    #     "session_history": history
    # })
    
    save_history_log(log_path, {
        "file_path": file_path,
        "session_history": history
    })

    return {
        "history": history,
        "final_status": "success" if not history[-1]["file_fixed"] else "max_attempts_reached"
    }

