def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

if __name__ == "__main__":
    file_path = r"F:\_Fast Drive (H)\A2Z-AI\13-AI_Agents_with_Pure_Python\AutoFix-AI\test_scripts\test_calculator.py"
    content = read_file(file_path)
    if content is not None:
        print("File content:\n")
        # print(content[0:20])
        print(content)




