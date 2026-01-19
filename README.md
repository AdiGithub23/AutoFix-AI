# AutoFix-AI

## Overview
AutoFix-AI is an Agentic AI application that automatically reads, executes, debugs, and fixes single-file Python scripts. It uses a Gemini API to analyze errors and apply corrections, repeating this process until the script runs successfully or a maximum attempts is reached.

## How It Works
1. Start the FastAPI application.
2. Submit the path to a local Python script via an API endpoint.
3. The system reads and executes the script.
4. Standard output, error output, and exit status are captured.
5. If execution fails, the system combines the code and output and sends them to the Gemini for analysis and correction suggestions.
6. If a fix is suggested, the file is updated and the process repeats.
7. The loop continues until the script runs without errors or the maximum iteration limit is reached.
8. All attempts and results are logged for future reference.

## Features
- Reads and executes local Python scripts
- Captures and analyzes script output and errors
- Uses Gemini LLM for code analysis and automated fixing
- Iterative, agentic loop with memory of past attempts
- Logs all sessions and adapts behavior based on history
- FastAPI backend for easy integration and testing

## Skills & Experience Gained
- **Agentic AI Design:** Built an autonomous loop with memory and adaptive behavior.
- **LLM Integration:** Used Gemini LLM for code analysis and automated fixes.
- **Python Scripting:** Automated file handling, subprocesses, and error management.
- **API Development:** Created a FastAPI backend for user interaction and workflows.
- **Stateful Logging:** Managed persistent logs to track memory and reasoning.
- **Debugging & Testing:** Tested and improved modules for script reading, execution and correction.

## Getting Started
1. Install dependencies from `requirements.txt`.
2. Set your Gemini API key in a `.env` file.
3. Start the FastAPI server:
	```
    uv venv _autofixai
    _autofixai\Scripts\activate
    uv pip install -r requirements.txt
    uvicorn src.app:app --reload
	```
4. Use the `/submit-file-path/` endpoint to submit a script for automated fixing.

## Project Structure
- `src/app.py` - FastAPI application and endpoints
- `src/agent/agent_code.py` - Agentic logic and LLM integration
- `src/agent/agent_functions.py` - File I/O, subprocess, and logging utilities


