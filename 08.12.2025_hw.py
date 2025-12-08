import cv2
import numpy as np
import ultralytics
from utils import get_angle

model = ultralytics.YOLO('yolo11s-pose.pt')

cap = cv2.VideoCapture(r'data/lesson_pose/squat.mp4')


lower_angle = 60
upper_angle = 165

counter = 0
move_down = True

while True:
    success, frame = cap.read()
    if not success:
        break

    results = model.predict(frame, verbose=False)[0]

    if results.keypoints is None:
        cv2.imshow("video", frame)
        cv2.waitKey(1)
        continue


    xy = results.keypoints.xy[0].cpu().numpy()


    x1, y1 = xy[12]   # бедро
    x2, y2 = xy[14]   # колено
    x3, y3 = xy[16]   # стопа

    angle = get_angle(x1, y1, x2, y2, x3, y3)


    if angle < lower_angle and move_down:
        move_down = False
        counter += 0.5

    if angle > upper_angle and not move_down:
        move_down = True
        counter += 0.5


    cv2.putText(frame, f"Angle: {int(angle)}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, f"Squats: {int(counter)}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.imshow("video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




    if angle < lower_angle and move_down:
        move_down = False
        counter += 0.5


    if angle > upper_angle and not move_down:
        move_down = True
        counter += 0.5


    cv2.putText(frame, f'Angle: {angle}', (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f'Squats: {int(counter)}', (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    for x, y in [xy[12], xy[14], xy[16]]:
        cv2.circle(frame, (int(x), int(y)), 8, (0, 0, 255), -1)

    cv2.imshow("video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
