import cv2
import mediapipe as mp


class DetectionLR:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.face = self.mp_face_mesh.FaceMesh(
            refine_landmarks=True,
            # static_image_mode=True,
            min_tracking_confidence=0.6,
            min_detection_confidence=0.6)

        self.WIDTH = 160
        self.HEIGHT = 90

        self.MIDDLE_POINT = self.WIDTH // 2
        self.LEFT_POINT = self.MIDDLE_POINT - 15
        self.RIGHT_POINT = self.MIDDLE_POINT + 15

        self.NOSE_IDX = 1

        self.DIRECTION_LEFT = "LEFT"
        self.DIRECTION_RIGHT = "RIGHT"
        self.DIRECTION_MID = "MID"

    def detect(self, img):
        results = self.face.process(img)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                coordinates = face_landmarks.landmark[self.NOSE_IDX]
                x = coordinates.x * self.WIDTH
                y = coordinates.y * self.HEIGHT

                if x < self.LEFT_POINT:
                    return self.DIRECTION_LEFT
                elif x > self.RIGHT_POINT:
                    return self.DIRECTION_RIGHT
                else:
                    return  self.DIRECTION_MID

    def draw(self, img):
        # middle line
        cv2.line(img, (self.MIDDLE_POINT, 0), (self.MIDDLE_POINT, self.HEIGHT), (0, 255, 0), 1)

        # left line
        cv2.line(img, (self.LEFT_POINT, 0), (self.LEFT_POINT, self.HEIGHT), (0, 0, 255), 1)

        # right line
        cv2.line(img, (self.RIGHT_POINT, 0), (self.RIGHT_POINT, self.HEIGHT), (0, 0, 255), 1)

        return img