import math


def calculate_angle(v1, v2):
    if v2[0] == v1[0]:
        if v2[1] > v1[1]:
            return 90
        else:
            return -90

    angle = math.degrees(math.atan2((v2[1] - v1[1]), (v2[0] - v1[0])))

    return -angle


def hand_vertical(hand_landmarks, mp_hands):

    index_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y,
    ]

    pinky_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y,
    ]

    if index_mcp[0] <= pinky_mcp[0]:
        angle = calculate_angle(index_mcp, pinky_mcp)
    else:
        angle = calculate_angle(pinky_mcp, index_mcp)

    if -30 < angle < 30:
        return True
    else:
        return False


def index_closed_horizontal(hand_landmarks, mp_hands):

    if (
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    ) < 0:
        return True

    elif (
        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    ) < 0:
        return True

    else:
        return False


def index_closed_vertical(hand_landmarks, mp_hands):

    if (
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    ) < 0:
        return True
    return False


def middle_closed_horizontal(hand_landmarks, mp_hands):

    if (
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
    ) < 0:
        return True

    elif (
        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
    ) < 0:
        return True

    else:
        return False


def middle_closed_vertical(hand_landmarks, mp_hands):

    if (
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
        - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    ) < 0:
        return True
    return False


def ring_closed_horizontal(hand_landmarks, mp_hands):

    if (
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
    ) < 0:
        return True

    elif (
        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
    ) < 0:
        return True

    else:
        return False


def ring_closed_vertical(hand_landmarks, mp_hands):

    if (
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
        - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
        - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    ) < 0:
        return True
    return False


def pinky_closed_horizontal(hand_landmarks, mp_hands):

    if (
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
    ) < 0:
        return True

    elif (
        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x
        - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
    ) < 0:
        return True

    else:
        return False


def pinky_closed_vertical(hand_landmarks, mp_hands):

    if (
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y
        - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
    ) * (
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
        - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
    ) < 0:
        return True
    return False


def thumb_pointing_up(hand_landmarks, mp_hands, check_thumbs_up=False):
    thumb_cmc = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y,
    ]
    thumb_tip = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y,
    ]

    angle = calculate_angle(thumb_cmc, thumb_tip)

    if 50 < angle < 130:
        if check_thumbs_up:
            if (
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
                - hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y
            ) > (
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
                - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
            ):
                return True
            else:
                return False
        return True
    else:
        return False


def thumb_pointing_down(hand_landmarks, mp_hands, check_thumbs_down=False):
    thumb_cmc = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y,
    ]
    thumb_tip = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y,
    ]

    angle = calculate_angle(thumb_cmc, thumb_tip)

    if -30 > angle > -150:
        if check_thumbs_down:
            if hand_vertical(hand_landmarks, mp_hands):
                if (
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                    - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
                ) > (
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
                    - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                ):
                    return True
            elif (
                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
            ) > (
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
                - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
            ):
                return True
            return False
        return True
    else:
        return False


def index_vertical_up(hand_landmarks, mp_hands):

    if index_closed_vertical(hand_landmarks, mp_hands):
        return False

    index_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y,
    ]
    index_tip = [
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
    ]

    angle = calculate_angle(index_mcp, index_tip)

    if index_mcp[1] < index_tip[1]:
        return False

    if 40 < angle < 140:
        return True
    else:
        return False


def middle_vertical_up(hand_landmarks, mp_hands):

    if middle_closed_vertical(hand_landmarks, mp_hands):
        return False

    middle_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y,
    ]
    middle_tip = [
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
    ]

    angle = calculate_angle(middle_mcp, middle_tip)

    if middle_mcp[1] < middle_tip[1]:
        return False

    if 40 < angle < 140:
        return True
    else:
        return False


def ring_vertical_up(hand_landmarks, mp_hands):

    if ring_closed_vertical(hand_landmarks, mp_hands):
        return False

    ring_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y,
    ]
    ring_tip = [
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y,
    ]

    angle = calculate_angle(ring_mcp, ring_tip)

    if ring_mcp[1] < ring_tip[1]:
        return False

    if 40 < angle < 140:
        return True
    else:
        return False


def pinky_vertical_up(hand_landmarks, mp_hands):

    if pinky_closed_vertical(hand_landmarks, mp_hands):
        return False

    pinky_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y,
    ]
    pinky_tip = [
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y,
    ]

    angle = calculate_angle(pinky_mcp, pinky_tip)

    if pinky_mcp[1] < pinky_tip[1]:
        return False

    if 40 < angle < 140:
        return True
    else:
        return False


def fist_closed(hand_landmarks, mp_hands):
    if (
        index_closed_horizontal(hand_landmarks, mp_hands)
        and middle_closed_horizontal(hand_landmarks, mp_hands)
        and ring_closed_horizontal(hand_landmarks, mp_hands)
        and pinky_closed_horizontal(hand_landmarks, mp_hands)
    ):
        return True
    else:
        return False


def stop_gesture(hand_landmarks, mp_hands):
    if (
        thumb_pointing_up(hand_landmarks, mp_hands)
        and index_vertical_up(hand_landmarks, mp_hands)
        and middle_vertical_up(hand_landmarks, mp_hands)
        and ring_vertical_up(hand_landmarks, mp_hands)
        and pinky_vertical_up(hand_landmarks, mp_hands)
    ):
        return True
    return False


def sign_gesture(hand_landmarks, mp_hands):
    if stop_gesture(hand_landmarks, mp_hands):
        return "Stop"
    if not fist_closed(hand_landmarks, mp_hands):
        return "Random"
    if thumb_pointing_up(hand_landmarks, mp_hands, check_thumbs_up=True):
        return "Thumbs Up"
    if thumb_pointing_down(hand_landmarks, mp_hands, check_thumbs_down=True):
        return "Thumbs Down"
    if hand_vertical(hand_landmarks, mp_hands):
        return "Neutral"
    return "Random"


def count_hand_orientation(hand_landmarks, mp_hands):

    wrist = [
        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,
    ]

    pinky_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y,
    ]

    angle = calculate_angle(wrist, pinky_mcp)
    if 60 <= angle <= 120:
        return "V"
    else:
        return "H"


def thumb_count_vertical(hand_landmarks, mp_hands):

    thumb_tip = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y,
    ]

    middle_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y,
    ]

    index_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y,
    ]

    index_pip = [
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x,
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y,
    ]

    # if (
    #     index_mcp[0] < thumb_tip[0] < pinky_mcp[0]
    #     or pinky_mcp[0] < thumb_tip[0] < index_mcp[0]
    # ):
    #     return False

    # return True
    dd1 = [1.15*(middle_mcp[0] - index_mcp[0]), index_mcp[0] - thumb_tip[0]]
    dd2 = [1.15*(middle_mcp[0] - index_mcp[0]), index_pip[0] - thumb_tip[0]]
    if dd1[0] < 0:
        dd1[0],dd1[1] = dd1[1],dd1[0]
        dd2[0],dd2[1] = dd2[1],dd2[0]
    
    if (
        dd1[0] < dd1[1] or dd2[0] < dd2[1]
    ):
        return True
    return False



def count_gesture(hand_landmarks, mp_hands, debug_mode = False):
    count = ""
    cnt = 0
    if count_hand_orientation(hand_landmarks, mp_hands) == "V":
        count += "_V_"
        count += "T" if thumb_count_vertical(hand_landmarks, mp_hands) else "*"
        count += "T" if not index_closed_vertical(hand_landmarks, mp_hands) and index_vertical_up(hand_landmarks, mp_hands) else "*"
        count += "T" if not middle_closed_vertical(hand_landmarks, mp_hands) and middle_vertical_up(hand_landmarks, mp_hands) else "*"
        count += "T" if not ring_closed_vertical(hand_landmarks, mp_hands) and ring_vertical_up(hand_landmarks, mp_hands) else "*"
        count += "T" if not pinky_closed_vertical(hand_landmarks, mp_hands) and pinky_vertical_up(hand_landmarks, mp_hands) else "*"

    else:
        count += "_H_"
        count += "T" if thumb_pointing_up(hand_landmarks, mp_hands) else "*"
        count += "T" if not index_closed_horizontal(hand_landmarks, mp_hands) else "*"
        count += "T" if not middle_closed_horizontal(hand_landmarks, mp_hands) else "*"
        count += "T" if not ring_closed_horizontal(hand_landmarks, mp_hands) else "*"
        count += "T" if not pinky_closed_horizontal(hand_landmarks, mp_hands) else "*"
    cnt = str(count.count("T"))
    if debug_mode:
        cnt+=count

    return cnt
