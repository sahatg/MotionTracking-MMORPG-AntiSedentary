import cv2
import mediapipe as mp
import pydirectinput
import time
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# --- SAKLAR (DEBOUNCING) ---
is_casting_1 = False
is_casting_2 = False
is_casting_aoe = False
is_drinking = False
is_walking = False
is_turning_left = False
is_turning_right = False
is_tabbing = False
is_mounting = False
is_jumping = False

# --- VARIABEL TIMER & HISTORI ---
last_step_time = 0
WALK_TIMEOUT = 0.7

shoulder_y_history = []

last_jump_time = 0
JUMP_COOLDOWN = 1.0

print("Sistem Aktif! Fitur Lengkap Siap Digunakan.")
print("Tekan tombol 'ESC' di jendela kamera untuk keluar dengan aman.")

while cap.isOpened():

    success, image = cap.read()

    if not success:
        continue

    # Mirror kamera
    image = cv2.flip(image, 1)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = pose.process(image_rgb)

    if results.pose_landmarks:

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        landmarks = results.pose_landmarks.landmark

        # =========================
        # EKSTRAKSI KOORDINAT
        # =========================

        nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y
        nose_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x

        r_wrist_y = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
        l_wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y

        r_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
        l_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y

        r_knee_y = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y
        l_knee_y = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y

        r_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
        l_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y

        r_wrist_x = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x
        l_wrist_x = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x

        r_shoulder_x = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x
        l_shoulder_x = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x

        r_hip_x = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x
        l_hip_x = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x

        wrist_distance = abs(r_wrist_x - l_wrist_x)

        avg_shoulder_y = (r_shoulder_y + l_shoulder_y) / 2
        avg_shoulder_x = (r_shoulder_x + l_shoulder_x) / 2
        avg_hip_x = (r_hip_x + l_hip_x) / 2

        current_time = time.time()

        # ==========================================
        # 1. LOGIKA LOMPAT (SPACE)
        # ==========================================

        shoulder_y_history.append(avg_shoulder_y)

        if len(shoulder_y_history) > 10:
            shoulder_y_history.pop(0)

        if (
            len(shoulder_y_history) == 10
            and (current_time - last_jump_time > JUMP_COOLDOWN)
        ):

            oldest_y = shoulder_y_history[0]

            jump_velocity_threshold = 0.05

            if (oldest_y - avg_shoulder_y) > jump_velocity_threshold:

                if not is_jumping:
                    pydirectinput.press('space')

                    is_jumping = True
                    last_jump_time = current_time

                cv2.putText(
                    image,
                    "LOMPAT! (SPACE)",
                    (10, 350),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )

            else:
                is_jumping = False

        else:
            is_jumping = False

        # ==========================================
        # 2. MOUNT (5)
        # ==========================================

        shoulder_width = abs(r_shoulder_x - l_shoulder_x)

        wrist_to_shoulder_ratio = (
            wrist_distance / (shoulder_width + 0.0001)
        )

        t_pose_ratio_threshold = 2.5

        is_t_pose = (
            wrist_to_shoulder_ratio > t_pose_ratio_threshold
            and r_wrist_y < r_hip_y
            and l_wrist_y < l_hip_y
            and r_wrist_y > nose_y
            and l_wrist_y > nose_y
        )

        if is_t_pose:

            if not is_mounting:
                pydirectinput.press('5')

                is_mounting = True

            cv2.putText(
                image,
                f"MOUNT MODE ({wrist_to_shoulder_ratio:.1f})",
                (10, 400),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (128, 0, 128),
                2
            )

        else:
            is_mounting = False

        # ==========================================
        # 3. TARGET TAB
        # ==========================================

        if wrist_distance < 0.08 and r_wrist_y > r_shoulder_y:

            if not is_tabbing:
                pydirectinput.press('tab')

                is_tabbing = True

            cv2.putText(
                image,
                "TARGET (TAB)",
                (10, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 255),
                2
            )

        else:
            is_tabbing = False

        # ==========================================
        # 4. GERAK KIRI KANAN
        # ==========================================

        lean_threshold = 0.04

        if not is_mounting:

            if avg_shoulder_x < avg_hip_x - lean_threshold:

                if not is_turning_left:
                    pydirectinput.keyDown('a')

                    is_turning_left = True

                if is_turning_right:
                    pydirectinput.keyUp('d')

                    is_turning_right = False

            elif avg_shoulder_x > avg_hip_x + lean_threshold:

                if not is_turning_right:
                    pydirectinput.keyDown('d')

                    is_turning_right = True

                if is_turning_left:
                    pydirectinput.keyUp('a')

                    is_turning_left = False

            else:

                if is_turning_left:
                    pydirectinput.keyUp('a')

                    is_turning_left = False

                if is_turning_right:
                    pydirectinput.keyUp('d')

                    is_turning_right = False

        # ==========================================
        # 5. KOMBAT
        # ==========================================

        dist_r_to_nose = math.hypot(
            r_wrist_x - nose_x,
            r_wrist_y - nose_y
        )

        dist_l_to_nose = math.hypot(
            l_wrist_x - nose_x,
            l_wrist_y - nose_y
        )

        drink_threshold = 0.1

        if (
            dist_r_to_nose < drink_threshold
            or dist_l_to_nose < drink_threshold
        ):

            if not is_drinking:
                pydirectinput.press('3')

                is_drinking = True

        elif (
            r_wrist_y < r_shoulder_y
            and l_wrist_y < l_shoulder_y
            and wrist_distance >= 0.08
        ):

            if not is_casting_aoe:
                pydirectinput.press('4')

                is_casting_aoe = True

        elif (
            r_wrist_y < r_shoulder_y
            and l_wrist_y > l_shoulder_y
            and wrist_distance >= 0.08
        ):

            if not is_casting_1:
                pydirectinput.press('1')

                is_casting_1 = True

        elif (
            l_wrist_y < l_shoulder_y
            and r_wrist_y > r_shoulder_y
            and wrist_distance >= 0.08
        ):

            if not is_casting_2:
                pydirectinput.press('2')

                is_casting_2 = True

        else:

            is_drinking = False
            is_casting_1 = False
            is_casting_2 = False
            is_casting_aoe = False

        # ==========================================
        # 6. BERJALAN (W)
        # ==========================================

        threshold_walk = 0.15

        is_stepping_now = (
            r_knee_y < r_hip_y + threshold_walk
            or l_knee_y < l_hip_y + threshold_walk
        )

        if is_stepping_now and not is_mounting:

            last_step_time = current_time

            if not is_walking:
                pydirectinput.keyDown('w')

                is_walking = True

        else:

            if (
                is_walking
                and (current_time - last_step_time > WALK_TIMEOUT)
            ):

                pydirectinput.keyUp('w')

                is_walking = False

    cv2.imshow('Motion Tracking WoW Mage', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# ==========================================
# CLEANUP
# ==========================================

if is_walking:
    pydirectinput.keyUp('w')

if is_turning_left:
    pydirectinput.keyUp('a')

if is_turning_right:
    pydirectinput.keyUp('d')

cap.release()
cv2.destroyAllWindows()