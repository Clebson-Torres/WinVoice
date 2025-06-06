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
                self.statusUpdate.emit("Fale: 'Computador'...")
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=10)
                    frase = self.recognizer.recognize_google(audio, language="pt-BR").lower()
                    print(f"🗣️ Ouvido: {frase}")
                    if self.hotword in frase:
                        self.hotwordDetected.emit(self.hotword)
                        self.statusUpdate.emit("chamada detectada! Processando...")
                        time.sleep(1)
                except sr.UnknownValueError:
                    self.statusUpdate.emit(f"Não entendi a chamada. Diga '{self.hotword}' para ativar.")
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
        # Loop principal do assistente, que só termina quando um comando é processado (executado/cancelado/saído)
        command_processed = False
        while not command_processed:
            entrada_comando = ""  # Variável para armazenar o comando reconhecido

            # --- Loop para obter o Comando Principal (O que você deseja?) ---
            comando_obtido_com_sucesso = False
            while not comando_obtido_com_sucesso:
                try:
                    self.assistantResponse.emit("O que você deseja que eu faça?", "")
                    self.falar("O que você deseja que eu faça?")

                    with self.mic as source:
                        self.recognizer.adjust_for_ambient_noise(source)
                        # Tempo limite maior para o comando principal
                        audio_comando = self.recognizer.listen(source, phrase_time_limit=10)

                    entrada_comando = self.recognizer.recognize_google(audio_comando, language="pt-BR").lower()
                    print(f"🗣️ Ouvido (Comando): {entrada_comando}")

                    if entrada_comando == "sair":
                        self.assistantResult.emit("Comando cancelado.", "Você pediu para sair.")
                        self.falar("Comando cancelado.")
                        command_processed = True  # Marca para sair do loop externo
                        comando_obtido_com_sucesso = True  # Marca para sair do loop atual
                        break  # Sai do loop de obter comando

                    self.commandRecognized.emit(entrada_comando)  # Emite o comando reconhecido para a UI
                    comando_obtido_com_sucesso = True  # Comando foi obtido com sucesso

                except sr.UnknownValueError:
                    self.errorOccurred.emit("Não entendi o que você disse. Por favor, repita ou diga 'sair'.")
                    self.falar("Não entendi o que você disse. Por favor, repita ou diga 'sair'.")
                    # Não muda comando_obtido_com_sucesso, então o loop continua e repete a pergunta
                except Exception as e:
                    self.errorOccurred.emit(
                        f"Erro no reconhecimento do comando: {e}. Por favor, tente novamente ou diga 'sair'.")
                    self.falar(f"Ocorreu um erro ao ouvir o comando: {e}. Por favor, tente novamente ou diga 'sair'.")
                    print(f"❌ Erro ao ouvir comando: {e}")
                    # Não muda comando_obtido_com_sucesso, então o loop continua e repete a pergunta

            # Se o comando foi "sair" (e command_processed se tornou True), sai do loop principal
            if command_processed:
                break

            # --- Processar o Comando Obtido (Gerar PowerShell) ---
            comando_powershell = self.gerar_comando(entrada_comando)
            print(f"\n[+] Comando PowerShell gerado: {comando_powershell}")
            self.assistantResponse.emit("Comando a ser executado:", comando_powershell)

            # --- Loop para obter a Confirmação ---
            confirmacao_obtida_com_sucesso = False
            while not confirmacao_obtida_com_sucesso:
                try:
                    self.falar("Deseja que eu execute esse comando?")
                    # Mantém o comando na UI enquanto pede confirmação
                    self.assistantResponse.emit("Deseja que eu execute esse comando?", comando_powershell)

                    with self.mic as source:
                        self.recognizer.adjust_for_ambient_noise(source)
                        # Tempo limite menor para confirmação
                        audio_confirmacao = self.recognizer.listen(source, phrase_time_limit=3)

                    confirmacao = self.recognizer.recognize_google(audio_confirmacao, language="pt-BR").lower()
                    print(f"🗣️ Transcrição da Confirmação: '{confirmacao}'")

                    # Lógica de confirmação mais flexível
                    if any(k in confirmacao for k in ["sim", "s", "pode", "ok", "confirma", "executar"]):
                        self.assistantResponse.emit("Executando comando...", comando_powershell)
                        resultado = self.executar_comando_powershell(comando_powershell)
                        print(f"\n[+] Resultado:\n{resultado}")
                        self.falar("Comando executado.")
                        self.assistantResult.emit("Comando executado!", resultado)
                        command_processed = True  # Marca para sair do loop principal
                        confirmacao_obtida_com_sucesso = True  # Marca para sair do loop de confirmação
                    elif any(k in confirmacao for k in ["não", "nao", "cancelar", "sair"]):
                        self.assistantResult.emit("Comando cancelado.", "")
                        self.falar("Comando cancelado.")
                        command_processed = True  # Marca para sair do loop principal
                        confirmacao_obtida_com_sucesso = True  # Marca para sair do loop de confirmação
                    else:  # Nenhuma das palavras-chave de confirmação/cancelamento foi detectada
                        self.errorOccurred.emit(
                            "Não entendi a confirmação. Por favor, diga 'sim' ou 'não' para este comando.")
                        self.falar("Não entendi a confirmação. Por favor, diga 'sim' ou 'não' para este comando.")
                        # Não muda confirmacao_obtida_com_sucesso, então o loop continua e repete a pergunta de confirmação

                except sr.UnknownValueError:
                    self.errorOccurred.emit(
                        "Não entendi a confirmação. Por favor, diga 'sim' ou 'não' para este comando.")
                    self.falar("Não entendi a confirmação. Por favor, diga 'sim' ou 'não' para este comando.")
                    # Não muda confirmacao_obtida_com_sucesso, então o loop continua e repete a pergunta de confirmação
                except Exception as e:
                    self.errorOccurred.emit(
                        f"Erro ao ouvir confirmação: {e}. Por favor, tente novamente ou diga 'sim'/'não'.")
                    self.falar(
                        f"Ocorreu um erro ao ouvir a confirmação: {e}. Por favor, tente novamente ou diga 'sim'/'não'.")
                    print(f"❌ Erro ao ouvir confirmação: {e}")
                    # Não muda confirmacao_obtida_com_sucesso, então o loop continua e repete a pergunta de confirmação

        # Só emite 'finished' quando o loop principal é encerrado
        if command_processed:
            self.finished.emit()