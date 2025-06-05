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


app_qt = QApplication(sys.argv)
assistant_ui = AssistantUI()


llm = OllamaLLM(model="gemma3:4b")
tts = pyttsx3.init()

APPS = {
    "the sims": r"C:\Program Files (x86)\DODI-Repacks\The Sims 4\Game\Bin\TS4_DX4_x64.exe", # Corrigi para DX4_x64.exe se for o caso
    "spotify": r"C:\Users\Clebs\AppData\Roaming\Spotify\Spotify.exe",
    "navegador": r"C:\Program Files\LibreWolf\librewolf.exe"
}

prompt_template = PromptTemplate.from_template("""
Você é um assistente que converte linguagem natural em comandos PowerShell válidos e seguros.
Sempre use a variável de ambiente $env:USERPROFILE para referenciar a pasta de usuário atual.
Usuário pediu: "{user_input}"
Responda apenas com o comando PowerShell, sem explicações.
""")

def gerar_comando_llm(user_input: str) -> str:
    for nome, caminho in APPS.items():
        if nome in user_input.lower():
            return f'Start-Process "{caminho}"'

    prompt = prompt_template.format(user_input=user_input)
    resposta = llm.invoke(prompt)
    print(f"Resposta do LLM: '{resposta.strip()}'")
    return resposta.strip()

def executar_comando_powershell_subprocess(comando: str) -> str:
    try:
        comandos = comando.strip().splitlines()
        saida_total = ""
        for cmd in comandos:
            resultado = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True,
                text=True,
                timeout=30
            )
            saida_total += resultado.stdout + resultado.stderr
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
assistant_worker_thread.finished.connect(lambda: hotword_listener_thread.statusUpdate.emit(f"Diga '{hotword_listener_thread.hotword}' para ativar."))



hotword_listener_thread.start()


sys.exit(app_qt.exec_())