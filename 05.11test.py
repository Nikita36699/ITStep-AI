import numpy as np

# # створення масиву
# array = np.array([1, 2, 3, 4, 5])
#
# print(array)
# print(array.shape)  # розмір масиву
# print(array.dtype)  # тип даних в одній комірці масиву
#
# # двовимірний масив(таблиця/матриця)
# array = np.array([[1, 2, 3, 4, 5],
#                   [6, 7, 8.5, 9, 10]])
#
# print(array)
# print(array.shape)  # розмір масиву
# print(array.dtype)  # тип даних в одній комірці масиву


# # порівнння швидкості для масивів та списків
# import time
#
#
# N = 10_000_000
# nums_list = list(range(N))
# nums_array = np.array(range(N))
#
# start = time.time()
# res = sum(nums_list)
# end = time.time()
#
# print(f"Python list: {end - start:0.5f} sec")
#
# start = time.time()
# res = np.sum(nums_array)
# end = time.time()
#
# print(f"Numpy array: {end - start:0.5f} sec")


# завжди використовувати функції numpy
# цикл for -- це велике зло

# # створення та розміри
#
# nums = np.arange(10, 20, 2)  # масив з діапазону, як в range
# print(nums)
#
# nums = np.zeros(shape=(3, 4))  # масив з нулів
# print(nums)
#
# # змінити розмір масиву
# nums = np.arange(10, 20)
# new_nums = nums.reshape((2, 5))
# print(new_nums)
# print(new_nums.shape)

# індексація
# nums = np.arange(10, 20)
#
# print(nums)
# # print(nums[2])
# # print(nums[2:5])  # зріз з 2(включно) по 5(не включно)
# # print(nums[2:7:2])  # зріз з 2(включно) по 7(не включно) крок 2
# # print(nums[:3])    # перші 3
# # print(nums[-3:])  # останні 3
#
# nums[2] = 0
#
# #nums[2:7] = 0
# nums[2:7] *= -1
#
# print(nums)

# nums = np.array([[1, 2, 3, 4, 5],
#                   [6, 7, 8.5, 9, 10]])
#
# print(nums.shape)  # рядки, стовпчики
# # для двовимірних масивів йже 2 індекса -- рядка та стовпчика
#
# print(nums[1, 2])    # 8.5
# print(nums[1])       # рядок з індексом 1
# print(nums[1, 2:4])  # рядок з індексом 1, стовпчики з 2 по 4
# print(nums[0:2, 1:4])  # блок рядки з 0 по 2 та стовпчики з 1 по 4
# print(nums[:, 3])    # стовпчик 3
#
# nums[0:2, 1:4] += 100
# print(nums)

#булеві маски
# nums = np.array([[1, 2, 3, 4, 5],
#                    [6, 7, 8.5, 9, 10]])
#
# mask = nums > 7
#
# print(mask)
# print(mask.dtype)
#
# print(nums[mask]) # дістати числа які відповідають масці(умові)
# nums[mask] = 0
# print(nums)
#
# # дістати числа які не відповідають масці(умові)
# # and = &
# #or = |
# #not =  ~
#
# print(nums[~mask])
#
#
# #кількість чисел що більше 7
# print(np.sum(mask))

# Завдання 1
# Створіть масив з числами від 1 до 10. Виведіть його, його розмір, тип даних.
# Змініть розмір масиву на (5, 2). Знову виведіть масив, розмір та тип даних
# nums = np.arange(1, 10 + 1)
# print(nums)
# print(nums.shape)
# print(nums.dtype)
#
# print(type(nums.shape))
#
#
# new_nums = nums.reshape((2, 5))
# print(new_nums)
# print(new_nums.shape)
# print(new_nums.dtype)
# # Завдання 2
# # Створіть масив:
# # 1 2 3 4 5 6 7 8 9 10 11 12
# # Використовуючи індекси виведіть:
# # ● число 7
# # ● другий рядок
# # ● останній стовпчик
# # ● праву половину
# # ● жовту область
# # ● замініть жовту область на -1
# # ● зробіть перший стовпчик таким самим як і другий
# new_array = np.arange(1, 12 + 1)
# new_array = new_array.reshape((3, 4))
#
# print(new_array[1, 2])
# print()
# print(new_array[2])
# print()
# print(new_array[0:3, 2:4])
# print()
# print(new_array[1:3, 1:3])
# print()
# new_array[1:3, 1:3] = -1
# print(new_array[1:3, 1:3])
# print()
# new_array[:, 0] = new_array[:, 1]
# print(new_array)
# # Завдання 3
# # У масиві з попереднього завдання створіть маску для чисел які більші за 6. З її допомогою
# # ● виведіть кількість чисел більших за 6
# # ● виведіть самі числа
# # ● до кожного числа яке відповідає масці додайте 10
# # ● кожне число що не відповідає масці помножте на -1
# # ● замініть ці числа які відповідають масці на відповідні їм з масиву
# # 1 0 1 0
# # 0 1 0 1
# # 1 0 1 0
# mask = new_array > 6
# print()
# print(np.sum(mask))
# print(new_array[mask])
# new_array[mask] += 10
# new_array[~mask] *= -1
#
# array = np.array([
#     [1, 0, 1, 0],
#     [0, 1, 0, 1],
#     [1, 0, 1, 0]
# ])
# print(array)
# print(mask)
#
# new_array[~mask] = array[~mask]
#
# print()
# print(new_array)
# print()
# Завдання 5
# Створіть масив та виведіть його тип даних
# 100 120 200 250 10

# Додайте до кожного числа 50 та виведіть результат.
# Створіть такий самий масив але з типом uint8
# Знову додайте 50 та виведіть результат

# Зробіть так щоб обчислення працювали правильно, якщо число виходить більшим за 255 то зробіть його 255
# array_new = np.array([100, 120, 200, 250, 10])
#
# array_new += 50
# print(array_new)
# print()
#
# array_new = np.array([100, 120, 200, 250, 10], dtype=np.uint8)
#
# # array_new += 50
# # print(array_new)
# # print()
#
# array_copy = array_new.astype(np.uint64)
# array_copy += 50
# print(array_copy)
#
# mask = array_copy > 255
#
# array_copy[mask] = 255
#
# print(array_copy[mask])



# array_copy = array_copy.astype(np.uint8)
# print(array_copy)


# Завдання 6
# Створіть масив типу uint8
# 10 4 25 40 200
# |Помножте всі значення на 2. Результат має бути типу uint8 а всі значення в діапазоні 0-255
# Помножте всі значення на 1.5. Результат має бути типу uint8 а всі значення в діапазоні 0-255

# nums = np.array([10, 4, 25, 40, 200], dtype=np.uint8)
# new_nums = nums.astype(np.uint64)
# new_nums *= 2
# mask =  new_nums > 255
# new_nums[mask] = 255
#
# nums = new_nums.astype(np.uint8)
# print(nums)


nums = np.array([10, 4, 25, 40, 200], dtype=np.uint8)
new_nums = nums.astype(np.float32)
print(new_nums)
new_nums *= 1.5
print(new_nums)
mask =  new_nums > 255
new_nums[mask] = 255
print(new_nums)
nums = new_nums.astype(np.uint8)
print(nums)