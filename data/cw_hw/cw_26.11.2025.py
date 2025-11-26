# детекція об'єктів(YOLO)

import ultralytics
import cv2
#
# # створення моделі
# model = ultralytics.YOLO('yolov8s.pt')
#
# # отримати зображення з ввідео
# cap = cv2.VideoCapture('data/lesson8/cars+bikes.mp4')
# success, img = cap.read()
#
# img = cv2.resize(img, None, fx=0.5, fy=0.5)
#
# cv2.imshow('original', img)
#
# # застосування моделі
# # predict може отримувати декілька зображень за раз
# # predict([img1, img2, img3]) і тому results це список
# # [result1, result2, result3]
#
# results = model.predict(
#     img,    # саме зображення
#     device='cpu',    # процесор де запускати модель
#                      # cpu -- звичайний процес
#                      # cuda -- графічний процесор
#     conf=0.25,       # мінімальній відсоток для об'єкта щоб попасти в result
#     iou=0.7      # максимально можливий рівень перетину рамок(якщо більше то вважаємо
#                  # що це рамки для одного й того самого об'єкта)
# )
#
#
# # results -- список з одним елементом
# result = results[0]
#
# # отримати назви класів(об'єкти які вмієме визначати модель)
# names = result.names # dict --- id: str
# print(names)
#
# # самі об'єкти
# cls = result.boxes.cls
# print(cls)
#
# # візуалізація результів
# res_img = result.plot()
# cv2.imshow('result', res_img)
#
#
# # ймовірності
# conf = result.boxes.conf
# print(conf)
#
#
# # рамка(box)
# boxes = result.boxes
#
# # отримати перший об'єкт
# box = boxes[0]
#
# print(box)
#
# # координати
# xyxy = box.xyxy[0]
#
# # переведення координат в int
# x1, y1, x2, y2 = map(int, xyxy)
#
# # вирізати об'єк з всього зображення
# # y -- відповідають за рядки
# # x -- відповідають за стовпчики
# roi = img[y1:y2, x1:x2]
#
# cv2.imshow('object', roi)
#
#
# # # відео
# # while True:
# #     success, img = cap.read()
# #
# #     if not success:
# #         break
# #
# #     img = cv2.resize(img, None, fx=0.5, fy=0.5)
# #
# #     results = model.predict(img)
# #     result = results[0]
# #
# #     res_img = result.plot()
# #
# #     cv2.imshow('result', res_img)
# #
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break
#
#
# cv2.waitKey(0)

# Завдання 1
# Отримайте перший кадр з файлу data\lesson8\animals.mp4 та виведіть його на екран.
# Проведіть детекцію об’єктів зо допомогою YOLO та виведіть результати.
# Змініть параметри моделі conf та iou і подивіться як це впливає на результат.
# Отримайте рамки для кожного об’єкта, виріжіть їх та виведіть як окремі зображення
import ultralytics
import cv2
from sympy import false

# створення моделі
model = ultralytics.YOLO('yolov8s.pt')

# отримати зображення з ввідео
cap = cv2.VideoCapture(r'C:\ITSTEP\ITStep-AI\data\lesson8\animals.mp4')
success, img = cap.read()

img = cv2.resize(img, None, fx=0.5, fy=0.5)


while True:
    success, img = cap.read()

    if not success:
        break

    img = cv2.resize(img, None, fx=0.5, fy=0.5)

    results = model.predict(
        img,  # саме зображення
        device='cpu',  # процесор де запускати модель
        # cpu -- звичайний процес
        # cuda -- графічний процесор
        conf=0.25,  # мінімальній відсоток для об'єкта щоб попасти в result
        iou=0.7 , # максимально можливий рівень перетину рамок(якщо більше то вважаємо
            # що це рамки для одного й того самого об'єкта)
        verbose=False
    )

    # results -- список з одним елементом
    result = results[0]

    # отримати назви класів(об'єкти які вмієме визначати модель)
    names = result.names  # dict --- id: str


    # самі об'єкти
    cls = result.boxes.cls


    # візуалізація результів
    res_img = result.plot()
    cv2.imshow('result', res_img)

    boxes = result.boxes

    # отримати перший об'єкт
    for i in range(len(boxes)):
        xyyy = boxes[i].xyxy
        box = boxes[i]

        x1, y1, x2, y2 = map(int, xyyy[0])
        roi = img[y1:y2, x1:x2]
        id = int(box.cls[0])
        name = result.names[id]

        cv2.imshow(f'roi-{name, i}', roi)


    cv2.imshow('result', res_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    print(result)



