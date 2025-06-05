# 🎙️  WinVoice

**WinVoice** é um assistente de voz offline para Windows que entende comandos em linguagem natural, converte para PowerShell com IA local, confirma por voz e executa no sistema. Ele escuta sua voz, responde com voz e mantém toda a privacidade localmente — sem internet.

---

## ✨ Funcionalidades

- 🎤 Reconhecimento de voz (em português)
- 🧠 Gera comandos PowerShell com IA local (`gemma3:4b`)
- 💬 Fala a resposta com voz (TTS)
- ✅ Confirmação por voz antes de executar
- 📁 Controla arquivos, programas e o sistema com comandos naturais
- 🔐 100% offline (modelo local via Ollama)

---

## 🚀 Como usar

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Clebson-Torres/WinVoice.git
   cd WinVoice
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instale o Ollama e baixe o modelo Gemma**
   ```bash
   ollama pull gemma3:4b
   ```

5. **Execute o assistente**
   ```bash
   python main.py
   ```

---

## 🎯 Exemplos de comandos por voz

- "Criar uma pasta chamada projetos na área de trabalho"
- "Mostrar os arquivos da pasta downloads"
- "Abrir o Spotify"
- "Encerrar o explorador de arquivos"
- "Desligar o computador"
- "Sair" → encerra o assistente

---

## 🧩 Requisitos

- Windows 10 ou superior
- Python 3.10+
- Ollama instalado e rodando
- Microfone configurado
- Placa de vídeo com suporte (ex: RTX 3050 ou superior)

---

## 📦 Dependências Python

- `langchain`
- `langchain-ollama`
- `pyttsx3`
- `SpeechRecognition`
- `pyaudio`

Instale com:
```bash
pip install -r requirements.txt
```

---

## 🔒 Privacidade

Este projeto é completamente **offline**. Nenhuma informação de voz, comando ou execução é enviada para a internet.

---

## 👨‍💻 Autor

**Clebson Torres**  
🔗 [github.com/Clebson-Torres](https://github.com/Clebson-Torres)

---

## 📜 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
