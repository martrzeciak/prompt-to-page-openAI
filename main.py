import os
from dotenv import load_dotenv
from openai import OpenAI



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


def get_openai_response(prompt):
    """
    Sends a prompt to the OpenAI API and returns the response.

    Parameters:
        prompt (str): The prompt to send to the API.

    Returns:
        str: The response from the API, or an error message if the request fails.
    """
    # Load the API key and set it for OpenAI's API client
    api_key = load_api_key()
    client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'], 
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    
    print(chat_completion)

    return chat_completion


def main():
    content = read_text_file("./article.txt")
    response = get_openai_response("Tell me something about dogs")
    # print(response)


if __name__ == "__main__":
    main()