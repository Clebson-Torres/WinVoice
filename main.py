import subprocess
import pyttsx3
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
import speech_recognition as sr

# Inicializa o modelo e a voz
llm = OllamaLLM(model="gemma3:4b")
tts = pyttsx3.init()

# Mapeamento direto de apps
APPS = {
    "the sims": r"C:\Program Files (x86)\DODI-Repacks\The Sims 4\Game\Bin\TS4_DX9_x64.exe",
    "spotify": r"C:\Users\Clebs\AppData\Roaming\Spotify\Spotify.exe",
    "navegador": r"C:\Program Files\LibreWolf\librewolf.exe"
}

# Template ajustado
prompt_template = PromptTemplate.from_template("""
Você é um assistente que converte linguagem natural em comandos PowerShell válidos e seguros.
Usuário pediu: "{user_input}"
Responda apenas com o comando PowerShell, sem explicações.
""")

def gerar_comando(user_input: str) -> str:
    for nome, caminho in APPS.items():
        if nome in user_input.lower():
            return f'Start-Process "{caminho}"'
    
    prompt = prompt_template.format(user_input=user_input)
    resposta = llm.invoke(prompt)
    return resposta.strip()

def executar_comando_powershell(comando: str) -> str:
    try:
        comandos = comando.strip().splitlines()
        saida_total = ""
        for cmd in comandos:
            resultado = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            saida_total += resultado.stdout + resultado.stderr
        return saida_total
    except Exception as e:
        return f"Erro ao executar: {e}"

def falar(texto):
    tts.say(texto)
    tts.runAndWait()

def ouvir_microfone(prompt=None):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    if prompt:
        falar(prompt)
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        return str(e)

def executar_assistente():
    entrada = ouvir_microfone("O que você deseja que eu faça?")
    if not entrada:
        falar("Não entendi o que você disse.")
        return

    comando = gerar_comando(entrada)
    print(f"\n[+] Comando PowerShell gerado: {comando}")

    falar("Deseja que eu execute esse comando?")
    confirmacao = ouvir_microfone()
    if confirmacao.lower() in ["sim", "s", "pode", "ok"]:
        resultado = executar_comando_powershell(comando)
        print(f"\n[+] Resultado:\n{resultado}")
        falar("Comando executado.")
    else:
        falar("Comando cancelado.")
