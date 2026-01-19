import os
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

def process_file(file_path):
    file_content = read_file(file_path)
    
    run_result = run_python_file(file_path)
    
    prompt = (
        "Here is a Python script:"
        "\n---\n"
        f"{file_content}"
        "\n---\n"
        "Here is its output:\n"
        f"STDOUT:\n{run_result['stdout']}\n"
        "\n---\n"
        f"STDERR:\n{run_result['stderr']}\n"
        f"Exit Code: {run_result['exit_code']}\n\n"
        "If there are any syntax errors, issues, or problems in the code or output, "
        "fix the code and return ONLY the corrected code. "
        "Add a comment wherever an update is made."
        "If there are no issues, return the original code."
    )

    # print("LLM Prompt:")
    # print(prompt)    
    # return {
    #     "file_content": file_content,
    #     "run_result": run_result,
    #     "llm_prompt": prompt
    # }
    
    llm_response = call_llm(prompt)
    # If the LLM response is different from the original, update the file
    if llm_response.strip() != file_content.strip():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(llm_response)
        fixed = True
    else:
        fixed = False

    print("LLM fix state:", fixed)

    return {
        "file_content": file_content,
        "run_result": run_result,
        "llm_prompt": prompt,
        "llm_response": llm_response,
        "file_fixed": fixed
    }

