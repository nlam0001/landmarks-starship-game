import cv2
import math
import mediapipe as mp

class GestureManager:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5
        )

    def get_gesture(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        gesture_name = "None"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibuja esqueleto de la mano en el feed de cámara
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                gesture_name = self.analyze_landmarks(hand_landmarks.landmark)
                
        return gesture_name, frame

    def analyze_landmarks(self, lm):
        """
        Determina el gesto analizando la posición relativa de los 21 puntos de la mano.
        """
        #DEDOS EXTENDIDOS
        index_out  = lm[8].y < lm[6].y
        middle_out = lm[12].y < lm[10].y
        ring_out   = lm[16].y < lm[14].y
        pinky_out  = lm[20].y < lm[18].y
        
        # Pulgar: Detectar si está extendido lateralmente (comparando con el índice)
        thumb_extended = abs(lm[4].x - lm[5].x) > 0.1

        # --- LÓGICA DE CLASIFICACIÓN ---

        # 1. Open_Palm (Mano abierta) -> Escudo
        if index_out and middle_out and ring_out and pinky_out:
            return "Open_Palm"

        # 2. Pointing_Up (Solo índice) -> Subir
        if index_out and not middle_out and not ring_out and not pinky_out:
            return "Pointing_Up"

        # 3. Victory (Índice y medio) -> Disparar
        if index_out and middle_out and not ring_out and not pinky_out:
            return "Victory"

        # 4. Rock_ON vs ILoveYou (Índice y meñique fuera)
        if index_out and pinky_out and not middle_out and not ring_out:
            if thumb_extended:
                return "ILoveYou" # Bomba
            return "Rock_ON"      # Ráfaga

        # 5. OK_Sign (Punta de pulgar toca punta de índice)
        dist_ok = math.sqrt((lm[4].x - lm[8].x)**2 + (lm[4].y - lm[8].y)**2)
        if dist_ok < 0.05 and middle_out and ring_out:
            return "OK_Sign" # Pausa

        # 6. Puño y Variantes de Pulgar (Dedos cerrados)
        if not index_out and not middle_out and not ring_out and not pinky_out:
            # Pulgar arriba
            if lm[4].y < lm[2].y - 0.06:
                return "Thumb_Up" # Super Carga
            # Pulgar abajo
            elif lm[4].y > lm[2].y + 0.06:
                return "Thumb_Down" # Bajar rápido
            # Puño cerrado
            else:
                return "Closed_Fist" # Cargar energía

        return "None"