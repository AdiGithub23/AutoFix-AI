import os
from google import genai
from dotenv import load_dotenv

def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    file_path = r"F:\_Fast Drive (H)\A2Z-AI\13-AI_Agents_with_Pure_Python\AutoFix-AI\test_scripts\test_calculator.py"
    content = read_file(file_path)
    if not content:
        exit(1)

    prompt = (
        "Here is a Python script:\n\n"
        f"{content}\n\n"
        "In a few words, what does this script do?"
    )

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    print("LLM Response:\n")
    print(response.text)