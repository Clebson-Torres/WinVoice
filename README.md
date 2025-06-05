# 🎙️ WinVoice

**WinVoice** is an offline voice assistant for Windows that understands natural language commands, converts them to PowerShell with local AI, confirms by voice, and executes them on the system. It listens to your voice, responds with voice, and maintains complete privacy locally — no internet required.

---

## ✨ Features

* 🎤 Voice recognition (in Portuguese)
* 🧠 Generates PowerShell commands with local AI (`gemma3:4b`)
* 💬 Speaks responses using Text-to-Speech (TTS)
* ✅ Voice confirmation before execution
* 📁 Controls files, programs, and the system with natural commands
* 🔐 100% offline (local model via Ollama)

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

Note: The Gemma model's (gemma3:4b) translation to PowerShell commands remains in Portuguese, but it can be adapted with more specific prompts if the input language is changed. Speech output (TTS) will also need to be adjusted if you want the assistant to speak in another language; this is done in pyttsx3 settings or by installing additional voice packages in Windows.
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
    ```bash
    ollama pull gemma3:4b
    ```

5.  **Run the assistant**
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
* "Sair" (Exit) → ends the assistant

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
