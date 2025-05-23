## Cloning the Repository:
```cmd
git clone https://github.com/martrzeciak/prompt-to-page-openAI.git
```
Navigating to the folder:
```cmd
cd prompt-to-page-openAI
```

## Before Running the Application:

Before the first launch, you need to run the `setup.bat` script, which will create a virtual environment, activate it, install all required libraries, and set up the necessary folder structure.

Run the script:
cmd
```cmd
setup.bat
```
***(Optional)**  
Opening the editor:
```cmd
code .
```
The script will install the libraries listed in the `requirements.txt` file:
```powershell
python-dotenv
openai
beautifulsoup4
requests
python-slugify
```
In the `.env` file, you must include your OpenAI API key: `OPENAI_API_KEY=your_api_key`. After modifying the file, restarting the terminal is required.

The following folder structure will also be created (if it does not already exist):
`root/output/images`.

## Running the Application:
Before running, ensure that you are in the project's root directory.
To launch the program, use the following command:
```python
python main.py
```
If the application runs successfully, the `output` directory will contain `artykul.html` and `podglad.html`, while all generated images will be stored in the `images` folder.

## Directory and File Description

- **📂 output**: Contains output files generated by the application.
  - `artykul.html`: Raw HTML code generated based on the article content.
  - `podglad.html`: A full preview with the applied template.
  - `images/`: Folder where AI-generated images are saved.

- **📂 prompts**: Contains files with prompt texts sent to the OpenAI API.
  - `generate_html_structure.txt`: Defines guidelines for generating HTML structure.
  - `generate_image.txt`: Prompt used for generating AI images.

- `main.py`: The main application script responsible for the entire process.

- `szablon.html`: A template with an empty `<body>` section.

- `article.txt`: The input file containing the article content to be processed.

- `.env`: Environment settings file, including the OpenAI API key.

- `requirements.txt`: A list of dependencies required by the application (e.g., `openai`, `beautifulsoup4`).

- `README.md`: The main project documentation file, containing installation and usage instructions.

- `setup.bat`: A script responsible for the initial setup.

**OS:**  Windows 11 23H2 | **Python**  3.13.0 | **pip** 24.2 

## Application functionality description

1. **Loading Environment Variables**  
The application loads environment variables from the `.env` file, including the OpenAI API key. This key is required for communication with OpenAI services. If the `OPENAI_API_KEY` variable is not set, the application will terminate with an appropriate error message.

2. **Logging Initialization**  
The application sets up logging to monitor its operation. All information, errors, and warnings are recorded in a log file with the date, logging level, and message.

3. **Loading Files**  
The application allows loading various input files:
   - `article.txt`: The article content to be processed.
   - `prompts/generate_html_structure.txt`: A prompt for generating the HTML structure based on the article.
   - `prompts/generate_image.txt`: A prompt for generating images.

4. **Generating HTML**  
After loading the files, the application combines the article content with the corresponding guidelines and sends a request to the OpenAI API to generate the HTML structure. The API returns HTML, which is then cleaned of unnecessary Markdown code and prepared for further processing.

5. **Generating Images**  
The application analyzes the generated HTML, extracting alt text from `<img>` tags. These texts serve as descriptions for the images to be generated. For each description:
   - A request is sent to OpenAI (DALL-E model) to create the corresponding image.
   - The image is downloaded and saved locally in the `output/images` folder.

7. **Modifying HTML**  
After generating and saving the images, the application updates the HTML by inserting the appropriate paths to the downloaded images in the `<img>` tags. Finally, the application saves the modified HTML to `artykul.html` and a full preview to `podglad.html`.
