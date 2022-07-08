# Run MediaPipe Hands.
import mediapipe as mp
import cv2
import argparse
from utils.camera import add_camera_args, Camera
import gestures

# import numpy as np
import time


def parse_args():

    parser = argparse.ArgumentParser()
    parser = add_camera_args(parser)
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    gst_str = (
        "v4l2src device=/dev/video{} ! "
        "video/x-raw, width=(int){}, height=(int){} ! "
        "videoconvert ! appsink"
    ).format(0, 640, 480)

    cam = cv2.VideoCapture(0)
    hands = mp_hands.Hands(
        static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7
    )

    while True:
        f, img = cam.read()
        name = "Res"
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
            (420, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
            False,
        )
        # print(curr_fps)
        # print(res.multi_handedness)

        if not res.multi_hand_landmarks:
            cv2.putText(
                img,
                "No_Hands",
                (0, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
                False,
            )
            cv2.imshow("Res", img)
            cv2.waitKey(1)
            continue
        # Draw hand landmarks of each hand.
        # print(f'Hand landmarks of {name}:')
        image_hight, image_width, _ = img.shape

        for hand_landmarks in res.multi_hand_landmarks:
            text = gestures.classify_gesture(hand_landmarks, mp_hands)
            cv2.putText(
                img,
                text,
                (0, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
                False,
            )
            annotated_image = cv2.flip(img.copy(), 1)
            mp_drawing.draw_landmarks(
                annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

        cv2.imshow("Res", cv2.flip(annotated_image, 1))
        cv2.waitKey(1)
