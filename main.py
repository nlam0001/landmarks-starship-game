import cv2
from detector import GestureManager
from juego import SpaceGame
import pygame

def main():
    # Inicializamos la cámara, el detector y el juego
    cap = cv2.VideoCapture(0)
    detector = GestureManager()
    game = SpaceGame()

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # 1. Espejo para que sea más fácil jugar
        frame = cv2.flip(frame, 1)

        # 2. Detectar el gesto
        gesto, frame = detector.get_gesture(frame)

        # 3. Pasar el gesto al juego y actualizar
        game.actualizar(gesto)
        game.dibujar()

        # 4. Mostrar la cámara en una ventana pequeña (opcional para la demo)
        cv2.imshow("Vision IA", frame)

        # Salir con la tecla 'q' o cerrando la ventana
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                return

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()