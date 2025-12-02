import ultralytics
import cv2
#
# model = ultralytics.YOLO('yolov8s.pt')
#
# cap = cv2.VideoCapture(r'C:\ITSTEP\ITStep-AI\data\lesson8\meetings.mp4')
#
# while True:
#     success, img = cap.read()
#     if not success:
#         break
#
#     img = cv2.resize(img, None, fx=0.5, fy=0.5)
#
#     results = model.predict(
#         img,
#         device='cpu',
#         conf=0.25,
#         iou=0.7,
#         verbose=False
#     )
#
#     result = results[0]
#     res_img = result.plot()
#
#     cv2.imshow('result', res_img)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break



model = ultralytics.YOLO('yolov8s.pt')

cap = cv2.VideoCapture(r'C:\ITSTEP\ITStep-AI\data\lesson8\meetings.mp4')

show_video = False

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, None, fx=0.5, fy=0.5)

    results = model.predict(
        img,
        device='cpu',
        conf=0.25,
        iou=0.7,
        verbose=False
    )

    result = results[0]

    cls = result.boxes.cls
    people_count = (cls == 0).sum().item()

    if people_count >= 5:
        show_video = True

    if show_video:
        res_img = result.plot()
        cv2.imshow('result', res_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
