import json
import logging
import os
import re
import requests
from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from slugify import slugify

# Load environment variables from a .env file
load_dotenv()

# Fetch the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if API key exists; exit if not found
if not openai_api_key:
    logging.error("Error: OPENAI_API_KEY not found. Make sure it is set in your .env file.")
    exit(1)
    
# Set up logging configuration   
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Formatter to preserve attribute order when working with BeautifulSoup
class UnsortedAttributes(HTMLFormatter):
    """
    Custom HTML formatter to ensure that attributes remain unsorted when using BeautifulSoup.
    """
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


def read_file(file_path, mode='r', encoding='utf-8'):
    """
    Reads the content of a file.

    :param file_path: Path to the file to read.
    :param mode: Mode to open the file (default is 'r').
    :param encoding: Encoding of the file (default is 'utf-8').
    :return: Content of the file as a string, or None if an error occurs.
    """
    
    # Check if the file exists at the provided file path
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None
    
    try:
        # Attempt to open the file in the specified mode and encoding
        with open(file_path, mode, encoding=encoding) as file:
            content = file.read()
        
        logging.info(f"File {file_path} successfully read.")
        
        return content
    except IOError as e:
        logging.error(f"Failed to read file {file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def save_html_to_file(html_code, output_path):
    """
    Saves HTML content to a file.

    :param html_code: HTML content as a string.
    :param output_path: Path to save the HTML file.
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            open(output_path, "w").close()
            
         # Write HTML content to the file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html_code)
            
        logging.info(f"HTML successfully saved to {output_path}")
    except IOError as e:
        logging.error(f"Failed to save HTML to {output_path}: {e}")


def extract_alt_texts(html_code):
    """
    Extracts 'alt' text from all <img> tags in the given HTML code.

    :param html_code: HTML content as a string.
    :return: List of 'alt' attributes found in <img> tags.
    """
    try:
        soup = BeautifulSoup(html_code, 'html.parser')
        
        # Find all 'img' tags and extract 'alt' attributes
        alt_texts = [img.get('alt') for img in soup.find_all('img') if img.get('alt')]
        
        logging.info(f"Extracted {len(alt_texts)} 'alt' attributes from <img> tags.")
        
        return alt_texts
    except Exception as e:
        logging.error(f"Error parsing HTML: {e}")
        return []


def insert_image_paths(html_code, image_names):
    """
    Updates the 'src' attribute of <img> tags in HTML with the provided image paths.

    :param html_code: HTML content as a string.
    :param image_names: List of image file names to insert as 'src' values.
    :return: Updated HTML content as a string.
    """
    if not image_names:
        logging.warning("No image paths provided. Returning original HTML.")
        return html_code

    try:
        soup = BeautifulSoup(html_code, "html.parser")
        
        logging.info("HTML template parsed successfully.")
        
        img_tags = soup.find_all("img")
        
        # Loop through each image tag and assign the corresponding image path
        for img_tag, img_path in zip(img_tags, image_names):
            img_tag['src'] = "images/" + img_path

        logging.info("Image paths successfully inserted into HTML.")
        
        # Return prettified HTML with attributes preserved
        return soup.prettify(formatter=UnsortedAttributes())
    except Exception as e:
        logging.error(f"Error inserting image paths: {e}")
        return html_code


def insert_content_into_html(template_html, content):
    """
    Inserts given content into the <body> tag of an HTML template.

    :param template_html: HTML template as a string.
    :param content: HTML content to insert into the <body> tag.
    :return: Updated HTML template with content inserted.
    """
    try:
        soup = BeautifulSoup(template_html, 'html.parser')
        
        logging.info("HTML template parsed successfully.")
        
        body_tag = soup.find('body')
        
        # Convert content into a BeautifulSoup object and append it to the body
        content_soup = BeautifulSoup(content, 'html.parser')
        body_tag.append(content_soup)
        
        logging.info("Content successfully inserted into <body> tag.")
        
        return soup.prettify()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def get_openai_response():
    """
    Generates HTML content using the OpenAI API based on prompts and article content.

    :return: HTML content as a string, or None if an error occurs.
    """
    article_content = read_file("./article.txt")
    generate_html_prompt = read_file("./prompts/generate_html_structure.txt")

    if not article_content or not generate_html_prompt:
        logging.error("Failed to read input files for OpenAI request.")
        return None
    
    client = OpenAI(api_key=openai_api_key)

    try:
        # Call OpenAI's API to generate HTML
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": generate_html_prompt + article_content},
            ],
            model="gpt-4o",
            temperature=1, # Control randomness in response
        )
        
        json_response = json.loads(response.to_json())
        html_content = json_response['choices'][0]['message']['content']

        logging.info("Successfully generated HTML using OpenAI.")
        
        # Clean up HTML by removing markdown code block
        pattern = r"^```html\n|```$"
        cleaned_response = re.sub(pattern, "", html_content, flags=re.MULTILINE)
        
        return cleaned_response
    except Exception as e:
        logging.error(f"Error interacting with OpenAI API: {e}")
        return None


def generate_image(description, prompt):
    """
    Generates an image using OpenAI's image generation API.

    :param description: Description of the image to be generated.
    :param prompt: Additional instructions or base prompt to refine the image generation.
    :return: URL of the generated image, or None if an error occurs.
    """
    client = OpenAI(api_key=openai_api_key)
    
    try:
        # Request image generation from OpenAI's DALL-E model
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt + description,
            size="1024x1024",
            quality="standard",
            n=1, # Generate one image
        )
        
        image_url = response.data[0].url
        
        logging.info("Image successfully generated.")
        
        return image_url
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return None


def download_image(image_url, image_name):
    """
    Downloads an image from the provided URL and saves it locally.

    :param image_url: URL of the image to download.
    :param image_name: Name to save the image file as.
    """
    try:
        # Send a GET request to download the image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open("./output/images/" + image_name, 'wb') as file:
                file.write(response.content)
            logging.info(f"Image downloaded and saved to {'./output/images/' + image_name}")
        else:
            logging.error(f"Failed to download image. HTTP status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
    

def process_images(image_descriptions):
    """
    Processes a list of image descriptions by generating and downloading images.

    :param image_descriptions: List of textual descriptions for the images to be generated.
    :return: List of names of the saved image files.
    """
    prompt = read_file("./prompts/generate_image.txt")
    image_names = []
    
    # Iterate through each description and process the images
    for description in image_descriptions:
        image_url = generate_image(description, prompt)
        if image_url:
            image_name = slugify(description) + ".jpg"
            download_image(image_url, image_name)
            image_names.append(image_name)
    return image_names


def main():
    """
    Main workflow to generate, update, and save HTML content and images.
    """
    try:
        image_names = []
        
        # Generate HTML content from OpenAI
        response = get_openai_response()
        
        if not response:
            logging.error("Failed to generate HTML content. Exiting...")
            return

        # Extract alt texts for images
        image_descriptions = extract_alt_texts(response)
        
        if image_descriptions:
            # Generate and download images
            image_names = process_images(image_descriptions)
            # Insert image paths into the HTML content
            response = insert_image_paths(response, image_names)
        
        # Save the final HTML content to a file            
        save_html_to_file(response, "./output/artykul.html")
        
        # Read the HTML template and insert content
        html_template = read_file("szablon.html")
        html_to_save = insert_content_into_html(html_template, response)
        save_html_to_file(html_to_save, "./output/podglad.html")
    except Exception as e:
        logging.error(f"An unexpected error occurred in the main flow: {e}")


if __name__ == "__main__":
    main()