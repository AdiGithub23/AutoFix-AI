from fastapi import FastAPI, Form
from src.agent.agent_code import process_file
from pydantic import BaseModel

# sample code file path: F:\_Fast Drive (H)\A2Z-AI\13-AI_Agents_with_Pure_Python\AutoFix-AI\src\runnable_files\test_calculator.py

app = FastAPI()

class FilePathRequest(BaseModel):
    file_path: str

@app.get("/")
def read_root():
    return {"message": "AutoFix-AI FastAPI backend is running."}

@app.post("/submit-file-path/")
def submit_file_path(file_path: str = Form(...)):
    result = process_file(file_path)
    return result

