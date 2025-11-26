# Завдання 1 Відкрийте відео з файлу data\lesson7\meter.mp4. Проведіть бінарізацію кадрів та збережіть в новий файл.
# Можливо очистіть від шуму або наведіть різкість через bilateralFilterimport cv2

import cv2

cap = cv2.VideoCapture(r'C:\ITSTEP\ITStep-AI\data\lesson7\meter.mp4')

if not cap.isOpened():
    print("Помилка: не вдалося відкрити відео")
    exit()

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Розмір фінального відео (в 2 рази менше)
new_size = (width // 2, height // 2)

writer = cv2.VideoWriter(
    'binary_meter.mp4',
    fourcc,
    fps,
    new_size,
    isColor=False
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Зменшуємо кадр
    frame = cv2.resize(frame, new_size)

    # Переводимо в GRAY
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Очищення шуму (м’яке, але не розмиває межі)
    denoise = cv2.bilateralFilter(gray, 9, 75, 75)

    # Бінаризація
    _, binary = cv2.threshold(denoise, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Записуємо в файл
    writer.write(binary)

    # Показ (по бажанню)
    cv2.imshow("binary", binary)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()