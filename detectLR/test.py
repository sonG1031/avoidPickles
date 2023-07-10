import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
face = mp_face_mesh.FaceMesh(refine_landmarks=True, static_image_mode=True, min_tracking_confidence=0.6, min_detection_confidence=0.6)

webcam = cv2.VideoCapture(1)

width = 160 # 1280
height = 90 # 180 # 720
middle_point = width // 2
NOSE_INDEX = 1

left_point = middle_point - 20
right_point = middle_point + 20

while webcam.isOpened():
    success, img = webcam.read()

    img = cv2.flip(img, 1)
    img = cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_LINEAR)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv는 BGR이라서 바꿔줘야함
    results = face.process(img)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # middle line
    cv2.line(img, (middle_point, 0), (middle_point, height), (0, 255, 0), 2)

    # left line
    cv2.line(img, (left_point, 0), (left_point, height), (0, 0, 255), 2)

    # right line
    cv2.line(img, (right_point, 0), (right_point, height), (0, 0, 255), 2)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            coordinates = face_landmarks.landmark[NOSE_INDEX]
            x = coordinates.x * width
            y = coordinates.y * height

            cv2.circle(img, (int(x), int(y)), 1, (255, 255, 255), 5)


            # print(f"x: {x}")
            if x < left_point:
                cv2.putText(img, "LEFT!",(0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv2.LINE_AA)
                # print(f"LEFT!! --> {x}")
            elif x > right_point:
                cv2.putText(img, "RIGHT!",(0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv2.LINE_AA)
                # print(f"RIGHT!! --> {x}")
    cv2.imshow("webcam", img)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyWindow("webcam")