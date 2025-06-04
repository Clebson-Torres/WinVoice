
import speech_recognition as sr
import time
from main import executar_assistente  

HOTWORD = "computador"  

def ouvir_em_background():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎙️ Assistente aguardando palavra-chave...")

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("🔎 Ouvindo...")
            audio = recognizer.listen(source, phrase_time_limit=5)

        try:
            frase = recognizer.recognize_google(audio, language="pt-BR").lower()
            print(f"🗣️ Ouvido: {frase}")

            if HOTWORD in frase:
                print("🟢 Palavra-chave detectada!")
                executar_assistente()
                print("🟡 Voltando a ouvir...")
        except sr.UnknownValueError:
            continue
        except Exception as e:
            print(f"❌ Erro: {e}")
            time.sleep(2)

if __name__ == "__main__":
    ouvir_em_background()
