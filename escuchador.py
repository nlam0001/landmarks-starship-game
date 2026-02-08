import speech_recognition as sr
import threading

class VoiceManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.7    # Tiempo de pausa para considerar el final de una frase
        self.recognizer.non_speaking_duration = 0.4 # Duración sin hablar antes de finalizar
        self.comando = "None"
        # Iniciamos el hilo para que escuche en segundo plano
        self.thread = threading.Thread(target=self.escuchar_continuo, daemon=True)
        self.thread.start()

    def escuchar_continuo(self):
        with sr.Microphone() as source:
            # Ajuste para ruido ambiental
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    audio = self.recognizer.listen(source)
                    texto = self.recognizer.recognize_google(audio, language="es-ES").lower()
                    print(f"Voz detectada: {texto}")
                    
                    # Filtramos los comandos
                    if "fuego" in texto or "dispara" in texto:
                        self.comando = "Victory"
                    elif "bomba" in texto:
                        self.comando = "ILoveYou"
                    elif "pausa" in texto:
                        self.comando = "OK_Sign"
                    elif "sube" in texto:
                        self.comando = "Pointing_Up"
                    elif "baja" in texto:
                        self.comando = "Thumb_Down"
                    elif "escudo" in texto:
                        self.comando = "Open_Palm"
                        
                except:
                    # Si no entiende nada, simplemente sigue escuchando
                    pass

    def get_command(self):
        # Devuelve el último comando y lo limpia
        cmd = self.comando
        self.comando = "None"
        return cmd