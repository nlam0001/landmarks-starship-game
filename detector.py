import cv2
import math

# MediaPipe 0.9.3.0 imports (stable legacy version with solutions API)
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class GestureManager:
    def __init__(self):
        self.mp_hands = mp_hands
        self.mp_draw = mp_drawing
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

    def get_gesture(self, frame):
        # MediaPipe usa RGB, OpenCV usa BGR
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        gesture_name = "None"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujamos las conexiones en el frame
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                gesture_name = self.analyze_landmarks(hand_landmarks.landmark)
                
        return gesture_name, frame

    def analyze_landmarks(self, lm):
        # Puntos clave: Pulgar(4), Índice(8), Medio(12), Anular(16), Meñique(20)
        # Nudillos base: Índice(6), Medio(10), Anular(14), Meñique(18)
        
        index_out = lm[8].y < lm[6].y
        middle_out = lm[12].y < lm[10].y
        ring_out = lm[16].y < lm[14].y
        pinky_out = lm[20].y < lm[18].y

        # 1. Pointing_Up (Solo índice)
        if index_out and not middle_out and not ring_out and not pinky_out:
            return "Pointing_Up"

        # 2. Victory (Índice y Medio)
        if index_out and middle_out and not ring_out and not pinky_out:
            return "Victory"

        # 3. Open_Palm (Todos arriba)
        if index_out and middle_out and ring_out and pinky_out:
            return "Open_Palm"

        # 4. Puño y Pulgares (Análisis del pulgar punto 4 vs punto 2)
        if not index_out and not middle_out and not ring_out and not pinky_out:
            if lm[4].y < lm[2].y - 0.05: return "Thumb_Up"
            if lm[4].y > lm[2].y + 0.05: return "Thumb_Down"
            return "Closed_Fist"

        # 5. I Love You (Pulgar, Índice y Meñique)
        if index_out and pinky_out and not middle_out and not ring_out:
            return "ILoveYou"

        return "None"
