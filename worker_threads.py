from PyQt5.QtCore import QThread, pyqtSignal
import speech_recognition as sr
import time


class HotwordListener(QThread):
    hotwordDetected = pyqtSignal(str)
    statusUpdate = pyqtSignal(str)

    def __init__(self, hotword="computador"):
        super().__init__()
        self.hotword = hotword
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self._running = True

    def run(self):
        self.statusUpdate.emit(f"Diga '{self.hotword}' para ativar.")
        while self._running:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.statusUpdate.emit("Ouvindo hotword...")
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    frase = self.recognizer.recognize_google(audio, language="pt-BR").lower()
                    print(f"🗣️ Ouvido: {frase}")
                    if self.hotword in frase:
                        self.hotwordDetected.emit(self.hotword)
                        self.statusUpdate.emit("Hotword detectada! Processando...")
                        time.sleep(1)
                except sr.UnknownValueError:
                    self.statusUpdate.emit(f"Não entendi a hotword. Diga '{self.hotword}' para ativar.")
                    continue
                except Exception as e:
                    self.statusUpdate.emit(f"Erro no reconhecimento da hotword: {e}")
                    print(f"❌ Erro Hotword: {e}")
                    time.sleep(2)

    def stop(self):
        self._running = False
        self.wait()


class AssistantWorker(QThread):
    commandRecognized = pyqtSignal(str)
    assistantResponse = pyqtSignal(str, str)
    assistantResult = pyqtSignal(str, str)
    errorOccurred = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, llm, tts, gerar_comando_func, executar_comando_powershell_func, falar_func):
        super().__init__()
        self.llm = llm
        self.tts = tts
        self.gerar_comando = gerar_comando_func
        self.executar_comando_powershell = executar_comando_powershell_func
        self.falar = falar_func
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def run(self):
        command_understood = False
        while not command_understood:
            try:
                self.assistantResponse.emit("O que você deseja que eu faça?", "")
                self.falar("O que você deseja que eu faça?")

                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)

                entrada = self.recognizer.recognize_google(audio,
                                                           language="pt-BR").lower()  # Converter para minúsculas aqui

                if entrada == "sair":  # Adicionar condição para sair do loop
                    self.assistantResult.emit("Comando cancelado.", "Você pediu para sair.")
                    self.falar("Comando cancelado.")
                    command_understood = True  # Sai do loop
                    continue  # Pula para o final do loop

                self.commandRecognized.emit(entrada)  # Emite o comando reconhecido para UI (opcional)

                comando = self.gerar_comando(entrada)
                print(f"\n[+] Comando PowerShell gerado: {comando}")
                self.assistantResponse.emit("Comando a ser executado:", comando)

                self.falar("Deseja que eu execute esse comando?")

                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                confirmacao = self.recognizer.recognize_google(audio, language="pt-BR").lower()

                if confirmacao in ["sim", "s", "pode", "ok"]:
                    self.assistantResponse.emit("Executando comando...", comando)
                    resultado = self.executar_comando_powershell(comando)
                    print(f"\n[+] Resultado:\n{resultado}")
                    self.falar("Comando executado.")
                    self.assistantResult.emit("Comando executado!", resultado)
                    command_understood = True  # Sai do loop
                else:
                    self.assistantResult.emit("Comando cancelado.", "")
                    self.falar("Comando cancelado.")
                    command_understood = True  # Sai do loop, pois o comando foi cancelado

            except sr.UnknownValueError:
                self.errorOccurred.emit("Não entendi o que você disse. Por favor, repita ou diga 'sair'.")
                self.falar("Não entendi o que você disse. Por favor, repita ou diga 'sair'.")
                # Não definimos command_understood = True aqui, para que o loop continue
            except Exception as e:
                self.errorOccurred.emit(f"Erro no assistente: {e}. Por favor, tente novamente ou diga 'sair'.")
                self.falar(f"Ocorreu um erro: {e}. Por favor, tente novamente ou diga 'sair'.")
                print(f"❌ Erro Assistente: {e}")
                # Também não definimos command_understood = True aqui
            finally:
                # Se o comando foi entendido ou o usuário saiu, o loop terminará na próxima iteração
                # caso contrário, ele continuará.
                if command_understood:
                    self.finished.emit()  # Sinaliza que o trabalho terminou apenas quando o loop realmente sair