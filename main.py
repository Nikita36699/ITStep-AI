import onnxruntime as ort
from  PIL import  Image
from torchvision import transforms
import  numpy as np


#dogs breeds
class_names = ['beagle',
 'bulldog',
 'dalmatian',
 'german-shepherd',
 'husky',
 'labrador-retriever',
 'poodle',
 'rottweiler']




#відкриваємо модель
session = ort.InferenceSession(
    "model.onnx"
)

#трансформер
test_transformer = transforms.Compose([
       transforms.Resize([224, 224]),
       transforms.ToTensor()
])


# отримати зображення
img = Image.open('data/lesson many/husky10.jpg')
img.show()

#застосувати трансформер
input_tensor = test_transformer(img)

#змінюємо shape(добавити 1)
input_tensor = input_tensor.unsqueeze(0)

#перевести в numpy

input_tensor = input_tensor.numpy()

# використати моделі
result = session.run(
    output_names=None, #отримати всі вхіднні данні
    input_feed={
        "image": input_tensor
    }
)

result = result[0][0]

#отримати індекс де найбільша ймовірність
ind = result.argmax()

# get class name
label = class_names[ind]

#отримати ймовірність
max_num = result.max()
result -= max_num
exp_result  = np.exp(result)
probs = exp_result / exp_result.sum()

prob = probs[ind]

print(probs)
print(f'index of the highest probability: {ind}')
print(f'dog breed: {label}')
print(f'Probability : {prob}')

