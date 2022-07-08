import mediapipe as mp
import cv2

# import argparse
# from utils.camera import add_camera_args, Camera
import classify_gestures

# import numpy as np
import time
from parameters import vertical_frame

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5
)
gesture_text = {
    "sign": "starting",
    "count": "starting"
}
set_gesture = False
print("############# MODEL LOADED ################")


def get_gesture_text():
    global gesture_text
    return gesture_text


def analyze(cam,mode="sign"):

    global hands, mp_hands, mp_drawing, gesture_text, set_gesture

    while True:
        set_gesture = False
        f, img = cam.read()
        if vertical_frame :
            img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
        if img is None:
            print("NONE")
            continue
        name = "Res"
        img = cv2.flip(img, 1)
        # cv2.imshow("RR",img)
        # cv2.waitKey(0)
        # cam.release()
        start = time.time()
        res = hands.process(cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 1))
        end = time.time()
        curr_fps = 1.0 / (end - start)
        cv2.putText(
            img,
            "FPS: " + str(round(curr_fps, 2)),
            (0, 450),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (203, 187, 157),
            2,
            cv2.LINE_AA,
            False,
        )
        # print(curr_fps)
        # print(res.multi_handedness)

        if not res.multi_hand_landmarks:
            gesture_text["sign"] = "No_Hands"
            gesture_text["count"] = "No_Hands"
            cv2.putText(
                img,
                "No_Hands",
                (0, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 158, 224),
                2,
                cv2.LINE_AA,
                False,
            )
            ret, jpeg = cv2.imencode(".jpg", img)
            frame = jpeg.tobytes()
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )
            # cv2.imshow("Res", img)
            # cv2.waitKey(1)
            continue
        # Draw hand landmarks of each hand.
        # print(f'Hand landmarks of {name}:')
        image_hight, image_width, _ = img.shape

        for hand_landmarks in res.multi_hand_landmarks:
            
            gesture_text["sign"] =  classify_gestures.sign_gesture(hand_landmarks, mp_hands)
            
            gesture_text["count"] = classify_gestures.count_gesture(hand_landmarks, mp_hands)
            
            cv2.putText(
                img,
                str(gesture_text),
                (0, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 158, 224),
                2,
                cv2.LINE_AA,
                False,
            )
            annotated_image = cv2.flip(img.copy(), 1)
            mp_drawing.draw_landmarks(
                annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )
        ret, jpeg = cv2.imencode(".jpg", cv2.flip(annotated_image, 1))
        frame = jpeg.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


#if not __name__ == "__main__":
#    cam = cv2.VideoCapture(0)
