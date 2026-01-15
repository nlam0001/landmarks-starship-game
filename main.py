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

        # 1. Obtener gesto de la IA
        gesto, frame = detector.get_gesture(frame)
        
        # 2. Actualizar lógica del juego
        # Si el juego devuelve False en alguna parte, cerramos
        game.actualizar(gesto)
        game.dibujar()

        # 3. Mostrar cámara para referencia
        cv2.putText(frame, f"IA GESTO: {gesto}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("Control de IA", frame)

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