import os
from dotenv import load_dotenv


def read_text_file(file_path):
    """
    Reads a text file and returns its content as a string.

    Parameters:
        file_path (str): The path to the text file.
    Returns:
        str: The contents of the file as a string.
    """
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



def load_api_key():
    """
    Loads the OpenAI API key from the environment variables.

    Returns:
        str: The OpenAI API key, or raises an exception if not found.
    """
    
    # Load environment variables from the .env file
    load_dotenv()

    # Retrieve the OpenAI API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("API key not found. Please make sure to set the OPENAI_API_KEY environment variable.")

    return api_key


def main():
    content = read_text_file("./article.txt")
    api_key = load_api_key()
    print(api_key)


if __name__ == "__main__":
    main()