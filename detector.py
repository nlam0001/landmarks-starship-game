import cv2
import math
import mediapipe as mp

class GestureManager:
    def __init__(self):
        # Usamos soluciones de mediapipe integradas
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
                # Dibuja esqueleto de la mano
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                gesture_name = self.analyze_landmarks(hand_landmarks.landmark)
                
        return gesture_name, frame

    def analyze_landmarks(self, lm):
        # DEDOS EXTENDIDOS (Comparando punta con nudillo)
        index_out  = lm[8].y < lm[6].y
        middle_out = lm[12].y < lm[10].y
        ring_out   = lm[16].y < lm[14].y
        pinky_out  = lm[20].y < lm[18].y
        
        # Pulgar extendido
        thumb_extended = abs(lm[4].x - lm[5].x) > 0.1

        # 1. Open_Palm (Mano abierta)
        if index_out and middle_out and ring_out and pinky_out:
            return "Open_Palm"

        # 2. Pointing_Up (Índice)
        if index_out and not middle_out and not ring_out and not pinky_out:
            return "Pointing_Up"

        # 3. Victory (Índice y medio)
        if index_out and middle_out and not ring_out and not pinky_out:
            return "Victory"

        # 4. Rock_ON vs ILoveYou
        if index_out and pinky_out and not middle_out and not ring_out:
            if thumb_extended: return "ILoveYou"
            return "Rock_ON"

        # 5. OK_Sign
        dist_ok = math.sqrt((lm[4].x - lm[8].x)**2 + (lm[4].y - lm[8].y)**2)
        if dist_ok < 0.05 and middle_out and ring_out:
            return "OK_Sign"

        # 6. Puño y Pulgar
        if not index_out and not middle_out and not ring_out and not pinky_out:
            if lm[4].y < lm[2].y - 0.06: return "Thumb_Up"
            elif lm[4].y > lm[2].y + 0.06: return "Thumb_Down"
            else: return "Closed_Fist"

        return "None"