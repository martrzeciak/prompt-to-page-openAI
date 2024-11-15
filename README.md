## Klonowanie repozytorium:
```cmd
git clone https://github.com/martrzeciak/prompt-to-page-openAI.git
```
Przejście do folderu:
```cmd
cd prompt-to-page-openAI
```

## Przed uruchomieniem aplikacji:  

Przed pierwszym uruchomieniem aplikacji należy uruchomić skrypt `setup.bat`, który stworzy wirtualne środowisko (virtual environment), aktywuje je, a następnie zainstaluje wszystkie potrzebne biblioteki i stworzy niezbędną strukturę folderów.

Uruchomienie skryptu:
cmd
```cmd
setup.bat
```
***(Opcjonalne)**  
Otwarcie edytora:
```cmd
code .
```
Skrypt zainstaluje biblioteki umieszone w pliku requirements.txt:
```powershell
python-dotenv
openai
beautifulsoup4
requests
python-slugify
```
W pliku `.env` umieścić należy klucz do API OpenAI: `OPENAI_API_KEY=your_api_key`. Po zmodyfikowaniu pliku konieczne jest ponowne uruchomienie terminala.

Zostanie również stworzona następująca struktura folderów (jeśli z jakiegoś powodu nie istnieją): `root/output/images`.

## Uruchomienie aplikacji:
Przed uruchomieniem należy upewnić się, że użytkownik znajduje się w głównym folderze projektu.
W celu uruchomienia programu należy użyć następującej komendy:
```python
python main.py
```
Jeśli działanie aplikacji zakończy się sukcesem w katalogu `output` zostaną umieszczone: `artykul.html` i `podglad.html`, natomiast w folderze `images` zostaną umieszczone wszystkie wygenerowane ilustracje.

## Opis katalogów i plików

- **📂 output**: Zawiera pliki wynikowe generowane przez aplikację.
  - `artykul.html`: Surowy kod HTML wygenerowany na podstawie treści artykułu.
  - `podglad.html`: Pełny podgląd z zastosowanym szablonem.
  - `images/`: Folder, w którym zapisywane są obrazy wygenerowane przez AI.

- **📂 prompts**: Zawiera pliki z treścią promptów wysyłanych do API OpenAI.
  - `generate_html_structure.txt`: Określa wytyczne do generowania struktury HTML.
  - `generate_image.txt`: Prompt używany do generowania grafik w AI.

- `main.py`: Główny skrypt aplikacji odpowiedzialny za całe działanie programu.

- `szablon.html`: Szablon z pustą sekcją `<body>`.

- `article.txt`: Plik wejściowy z treścią artykułu, który ma być przetwarzany.

- `.env`: Plik z ustawieniami środowiska, w tym kluczem API dla OpenAI.

- `requirements.txt`: Lista zależności wymaganych przez aplikację (np. `openai`, `beautifulsoup4`).

- `README.md`: Główny plik dokumentacyjny projektu, zawierający opis instalacji i użytkowania.

- `setup.bat`: Skrypt odpowiedzialny za wstępną konfigurację.

**OS:**  Windows 11 23H2 | **Python**  3.13.0 | **pip** 24.2 
