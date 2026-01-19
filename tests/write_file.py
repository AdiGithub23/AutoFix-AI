def write_file(file_path, content):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("\nContent written successfully!")
    except Exception as e:
        print(f"Error writing to file: {e}")

def append_to_file(file_path, content):
    try:
        with open(file_path, "a", encoding="utf-8") as f:  # Use "a" for append mode
            f.write(content)
        print("\nContent appended successfully!")
    except Exception as e:
        print(f"Error writing to file: {e}")


if __name__ == "__main__":
    file_path = r"F:\_Fast Drive (H)\A2Z-AI\13-AI_Agents_with_Pure_Python\AutoFix-AI\test_scripts\test_calculator.py"
    content = "\n\n# test_scripts/test_calculator.py"
    # write_file(file_path, content)
    append_to_file(file_path, content)







