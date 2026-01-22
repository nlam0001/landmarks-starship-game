import cv2
from detector import GestureManager
from juego import SpaceGame
import pygame
import sys

def main():
    cap = cv2.VideoCapture(0)
    detector = GestureManager()
    game = SpaceGame()

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        frame = cv2.flip(frame, 1)

        # Obtiene el gesto de la cámara
        gesto, frame = detector.get_gesture(frame)
        
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