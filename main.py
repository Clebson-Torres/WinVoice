import subprocess
import pyttsx3
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
import speech_recognition as sr
import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QCoreApplication
from ui_manager import AssistantUI
from worker_threads import HotwordListener, AssistantWorker
from prompts import POWERSHELL_COMMAND_PROMPT
import urllib.parse  # NOVO: Importar para codificação de URL

app_qt = QApplication(sys.argv)
assistant_ui = AssistantUI()

llm = OllamaLLM(model="gemma3:4b")
tts = pyttsx3.init()

APPS = {
    "the sims": r"C:\Program Files (x86)\DODI-Repacks\The Sims 4\Game\Bin\TS4_DX4_x64.exe",
    "spotify": r"C:\Users\Clebs\AppData\Roaming\Spotify\Spotify.exe",
    "navegador": r"C:\Program Files\LibreWolf\librewolf.exe"
}

WEBSITES = {
    "g1": "https://g1.globo.com",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "twitter": "https://x.com",
    "whatsapp web": "https://web.whatsapp.com"
}

prompt_template = PromptTemplate.from_template(POWERSHELL_COMMAND_PROMPT)


def gerar_comando_llm(user_input: str) -> str:
    user_input_lower = user_input.lower()

    # 1. Verificar Mapeamento Direto de Aplicativos
    for nome_app, caminho_app in APPS.items():
        if nome_app in user_input_lower:
            return f'Start-Process "{caminho_app}"'

    # 2. Verificar Mapeamento Direto de Sites
    for nome_site, url_site in WEBSITES.items():
        if nome_site in user_input_lower:
            return f'Start-Process "{url_site}"'

    # 3. NOVO: Lógica para Pesquisa no Google
    search_keywords = ["pesquisar por", "procurar por", "buscar por", "pesquisar", "procurar", "buscar"]
    for keyword in search_keywords:
        if keyword in user_input_lower:
            search_query_raw = user_input_lower.split(keyword, 1)[1].strip()
            if search_query_raw:  # Garante que há algo para pesquisar
                # Codifica a consulta para URL
                search_query_encoded = urllib.parse.quote_plus(search_query_raw)
                google_search_url = f"https://www.google.com/search?q={search_query_encoded}"
                return f'Start-Process "{google_search_url}"'

    # 4. Tentar Extrair URL diretamente se "acessar" ou "abrir o site" for usado
    if "acessar" in user_input_lower or "abrir o site" in user_input_lower:
        parts = user_input_lower.split()
        for part in parts:
            if "." in part and (
                    "http" in part or "www" in part or part.endswith(".com") or part.endswith(".br") or part.endswith(
                    ".org")):
                if not part.startswith("http"):
                    part = "https://" + part
                return f'Start-Process "{part}"'

    # 5. Usar o LLM para gerar o comando se as verificações diretas falharem
    prompt = prompt_template.format(user_input=user_input)
    resposta = llm.invoke(prompt)
    raw_command = resposta.strip()

    # Lógica para remover backticks (formatação de código)
    if raw_command.startswith('`') and raw_command.endswith('`'):
        raw_command = raw_command.strip('`')
    elif raw_command.startswith('```') and raw_command.endswith('```'):
        raw_command = raw_command.strip('`').strip()
        if raw_command.lower().startswith('powershell'):
            raw_command = raw_command[len('powershell'):].strip()

    print(f"Resposta do LLM (limpa): '{raw_command}'")
    return raw_command


def executar_comando_powershell_subprocess(comando: str) -> str:
    try:
        comandos = comando.strip().splitlines()
        saida_total = ""
        for cmd in comandos:
            resultado = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True,
                text=True,
                encoding='cp1252',
                errors='replace',
                timeout=30
            )
            saida_total += (resultado.stdout or '') + (resultado.stderr or '')
        return saida_total
    except Exception as e:
        return f"Erro ao executar: {e}"


def falar_tts(texto):
    tts.say(texto)
    tts.runAndWait()


hotword_listener_thread = HotwordListener(hotword="computador")
assistant_worker_thread = AssistantWorker(
    llm=llm,
    tts=tts,
    gerar_comando_func=gerar_comando_llm,
    executar_comando_powershell_func=executar_comando_powershell_subprocess,
    falar_func=falar_tts
)

hotword_listener_thread.statusUpdate.connect(assistant_ui.update_status_message)
hotword_listener_thread.hotwordDetected.connect(assistant_worker_thread.start)

assistant_worker_thread.assistantResponse.connect(assistant_ui.show_command_and_status)
assistant_worker_thread.assistantResult.connect(assistant_ui.show_final_result)

assistant_worker_thread.errorOccurred.connect(assistant_ui.update_status_message)

assistant_worker_thread.finished.connect(assistant_ui.hide_window)
assistant_worker_thread.finished.connect(
    lambda: hotword_listener_thread.statusUpdate.emit(f"Diga '{hotword_listener_thread.hotword}' para ativar."))

hotword_listener_thread.start()

sys.exit(app_qt.exec_())