import json
import logging
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from slugify import slugify

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    logging.error("Error: OPENAI_API_KEY not found. Make sure it is set in your .env file.")
    exit(1)
    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


def read_file(file_path, mode='r', encoding='utf-8'):
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None
    try:
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
    try:
        if not os.path.exists(output_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            open(output_path, "w").close()
            
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html_code)
            
        logging.info(f"HTML successfully saved to {output_path}")
    except IOError as e:
        logging.error(f"Failed to save HTML to {output_path}: {e}")


def extract_alt_texts(html_code):
    try:
        soup = BeautifulSoup(html_code, 'html.parser')
        alt_texts = [img.get('alt') for img in soup.find_all('img') if img.get('alt')]
        
        logging.info(f"Extracted {len(alt_texts)} 'alt' attributes from <img> tags.")
        
        return alt_texts
    except Exception as e:
        logging.error(f"Error parsing HTML: {e}")
        return []


def insert_image_paths(html_code, image_names):
    if not image_names:
        logging.warning("No image paths provided. Returning original HTML.")
        return html_code

    try:
        soup = BeautifulSoup(html_code, "html.parser")
        
        logging.info("HTML template parsed successfully.")
        
        img_tags = soup.find_all("img")

        for img_tag, img_path in zip(img_tags, image_names):
            img_tag['src'] = "images/" + img_path

        logging.info("Image paths successfully inserted into HTML.")
        
        return soup.prettify(formatter=UnsortedAttributes())
    except Exception as e:
        logging.error(f"Error inserting image paths: {e}")
        return html_code


def insert_content_into_html(template_html, content):
    try:
        soup = BeautifulSoup(template_html, 'html.parser')
        
        logging.info("HTML template parsed successfully.")
        
        body_tag = soup.find('body')
        
        content_soup = BeautifulSoup(content, 'html.parser')
        body_tag.append(content_soup)
        
        logging.info("Content successfully inserted into <body> tag.")
        
        return soup.prettify()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def get_openai_response():
    article_content = read_file("./article.txt")
    generate_html_prompt = read_file("./prompts/generate_html_structure.txt")

    if not article_content or not generate_html_prompt:
        logging.error("Failed to read input files for OpenAI request.")
        return None
    
    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": generate_html_prompt + article_content},
            ],
            model="gpt-4o-mini",
            temperature=1,
        )
        
        json_response = json.loads(response.to_json())
        html_content = json_response['choices'][0]['message']['content']
        
        logging.info("Successfully generated HTML using OpenAI.")
        
        return html_content
    except Exception as e:
        logging.error(f"Error interacting with OpenAI API: {e}")
        return None


def generate_image(description):
    prompt = read_file("./prompts/generate_image.txt")
    client = OpenAI(api_key=openai_api_key)
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt + description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        logging.info("Image successfully generated.")
        return image_url
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return None


def download_image(image_url, image_name):
    try:
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
    image_names = []
    for description in image_descriptions:
        image_url = generate_image(description)
        if image_url:
            image_name = slugify(description) + ".jpg"
            download_image(image_url, image_name)
            image_names.append(image_name)
    return image_names


def main():
    try:
        image_names = []
        response = get_openai_response()
        
        if not response:
            logging.error("Failed to generate HTML content. Exiting...")
            return

        image_descriptions = extract_alt_texts(response)
        
        if image_descriptions:
            image_names = process_images(image_descriptions)
            response = insert_image_paths(response, image_names)
                    
        save_html_to_file(response, "./output/artykul.html")
        
        html_template = read_file("szablon.html")
        html_to_save = insert_content_into_html(html_template, response)
        save_html_to_file(html_to_save, "./output/podglad.html")
    except Exception as e:
        logging.error(f"An unexpected error occurred in the main flow: {e}")


if __name__ == "__main__":
    main()