
"""
Reads a text file and returns its content as a string.
Parameters:
file_path (str): The path to the text file.
Returns:
str: The contents of the file as a string.
"""
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except IOError:
        print("Error: An I/O error occurred.")
        return None

def main():
    content = read_text_file("./article.txt")
    print(content)

if __name__ == "__main__":
    main()