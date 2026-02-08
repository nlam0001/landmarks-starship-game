import cv2
from detector import GestureManager
from juego import SpaceGame
from escuchador import VoiceManager
import pygame
import sys
import os 

def resource_path(relative_path):
    """ Función necesaria para que el .exe encuentre los archivos (imágenes/sonidos) """
    try:
        
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    # Inicia Pygame antes para evitar errores de carga
    pygame.init()
    
    cap = cv2.VideoCapture(0)
    detector = GestureManager()

    game = SpaceGame()
    voice_manager = VoiceManager()

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        frame = cv2.flip(frame, 1)

        # Obtiene el gesto de la cámara
        gesto, frame = detector.get_gesture(frame)
        
        # Obtiene el comando de voz
        comando_voz = voice_manager.get_command()
        if comando_voz != "None":
            gesto = comando_voz # Prioriza comando de voz si hay

        # Lógica del juego
        game.actualizar(gesto)
        game.dibujar()

        # Mostrar cámara para referencia
        cv2.putText(frame, f"GESTO: {gesto}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("Detector de gestos", frame)

        # Salidas estándar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()