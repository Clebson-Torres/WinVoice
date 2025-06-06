# 🎙️ WinVoice

**WinVoice** is an offline voice assistant for Windows that understands natural language commands, converts them to PowerShell with local AI, confirms by voice, and executes them on the system. It listens to your voice, responds with voice, and maintains complete privacy locally — no internet required.

---

## ✨ Features

* 🎤 Voice recognition
* 🧠 Generates PowerShell commands with local AI (`gemma3:4b`)
* 💬 Speaks responses using Text-to-Speech (TTS)
* ✅ Voice confirmation before execution
* 📁 Controls files, programs, and the system with natural commands

---
## ⚙️ Language Configuration

Voice recognition uses Google's speech recognition service, which supports various languages via BCP-47 codes (RFC 5646). The default language configured in WinVoice is Brazilian Portuguese (pt-BR).

To change the recognition language:

Open the worker_threads.py file.

Locate the following lines within the HotwordListener and AssistantWorker classes, where recognize_google is called:

    # Inside HotwordListener.run()
    frase = self.recognizer.recognize_google(audio, language="pt-BR").lower()

    # Inside AssistantWorker.run()
    entrada = self.recognizer.recognize_google(audio, language="pt-BR").lower()
    
    # And also for confirmation
    confirmacao = self.recognizer.recognize_google(audio, language="pt-BR").lower()


Replace "pt-BR" with the desired language code.
    
Examples of language codes:

        English (US): en-US

        Spanish (Spain): es-ES

        French: fr-FR

        German: de-DE

        Japanese: ja-JP

For a more comprehensive list of language codes, consult the SpeechRecognition library documentation or a list of BCP-47 codes.

Note: The Gemma model's (gemma3:4b) translation to PowerShell commands remains in Portuguese, but it can be adapted with more specific prompts if the input language is changed.

## 📝 Prompt Language Adaptation

The core intelligence of WinVoice, specifically how it understands your natural language and converts it into PowerShell commands, is guided by the POWERSHELL_COMMAND_PROMPT located in prompts.py. This prompt includes instructions, rules, and examples for the local AI model (Gemma).

For the AI to accurately generate commands, the language of the prompt MUST match the language you are speaking.

To adapt WinVoice for other languages:

Create Language-Specific Prompt Files:
Duplicate prompts.py for each language you want to support. For example:

        prompts_en.py (a new file for English prompts)

        prompts_es.py (a new file for Spanish prompts)

Translate the entire POWERSHELL_COMMAND_PROMPT string within these new files into the respective language. Ensure that the instructions, rules, and all examples are accurately translated, including the PowerShell command examples themselves if they need to change based on language-specific phrasing.

Update main.py to Import the Desired Language Prompt:
    Open main.py and modify the import statement to point to the correct language file.

Example: To use English prompts:

Find this line:

    from prompts import POWERSHELL_COMMAND_PROMPT

And change it to:

    from prompts_en import POWERSHELL_COMMAND_PROMPT # Or prompts_es, etc.

(Remember to save both main.py and the new prompt file.)

By following these steps for both speech recognition and the AI prompt, you can configure WinVoice to operate in your preferred language.
## 🚀 How to Use

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Clebson-Torres/WinVoice.git](https://github.com/Clebson-Torres/WinVoice.git)
    cd WinVoice
    ```

2.  **Create and activate the virtual environment**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Ollama and download the Gemma model**
    https://ollama.com/download
    ```bash
    ollama pull gemma3:4b
    ```

6.  **Run the assistant**
    ```bash
    python main.py
    ```

---

## 🎯 Voice Command Examples

* "Criar uma pasta chamada projetos na área de trabalho" (Create a folder called projects on the desktop)

* "Mostrar os arquivos da pasta downloads" (Show files in the downloads folder)

* "Abrir o Spotify" (Open Spotify)

* "Encerrar o explorador de arquivos" (Close File Explorer)

* "Desligar o computador" (Shut down the computer)

* "Abrir a pasta de documentos" (Open the documents folder)

* "Abrir o site do YouTube" (Open the YouTube website)

* "Pesquisar por previsão do tempo em São Paulo" (Search for weather forecast in São Paulo)

* "Procurar por notícias de tecnologia" (Look for technology news)

* "Buscar por restaurantes italianos próximos" (Search for nearby Italian restaurants)

* "Aumentar o volume" (Increase volume)

* "Diminuir o volume" (Decrease volume)

* "Sair" (Exit) → This command ends the assistant and returns it to the hotword waiting state.

---

## 🧩 Requirements

* Windows 10 or higher
* Python 3.10+
* Ollama installed and running
* Microphone configured
* Supported graphics card (e.g., RTX 3050 or higher)
* If a compatible GPU is not available, Ollama will use the CPU for inference, which may result in slower performance depending on the model and your processor.

---

## 📦 Python Dependencies

* `langchain`
* `langchain-ollama`
* `pyttsx3`
* `SpeechRecognition`
* `pyaudio`
* `PyQt5`

 Install with:
 
 ```pip install -r requirements.txt```

## 🔒 Privacy
This project is completely offline. No voice data, commands, or executions are sent to the internet

---

## 👨‍💻 Autor

**Clebson Torres**  
🔗 [github.com/Clebson-Torres](https://github.com/Clebson-Torres)

---

## 📜 License

Distributed under the MIT License. See the LICENSE file for more details.
