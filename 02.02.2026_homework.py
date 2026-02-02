import onnxruntime as ort
import torch
from  PIL import  Image
from torchvision import transforms
import  numpy as np

test_transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

class_names = [
    "Apple Braeburn",
    "Apple Granny Smith",
    "Apricot",
    "Avocado",
    "Banana",
    "Blueberry",
    "Cactus fruit",
    "Cantaloupe",
    "Cherry",
    "Clementine",
    "Corn",
    "Cucumber Ripe",
    "Grape Blue",
    "Kiwi",
    "Lemon",
    "Limes",
    "Mango",
    "Onion White",
    "Orange",
    "Papaya",
    "Passion Fruit",
    "Peach",
    "Pear",
    "Pepper Green",
    "Pepper Red",
    "Pineapple",
    "Plum",
    "Pomegranate",
    "Potato Red",
    "Raspberry",
    "Strawberry",
    "Tomato",
    "Watermelon"
]


session = ort.InferenceSession('homework_NN.onnx')

image = Image.open('data/lesson many/fruits/55.jpg')

input_tensor: torch.Tensor = test_transform(image)

input_tensor = input_tensor.unsqueeze(0)



input_tensor = input_tensor.numpy()


result = session.run(
    output_names=None,
    input_feed={
        "input": input_tensor
    }
)


result  = result[0][0]


ind = result.argmax()


label = class_names[ind]



result_tensor = torch.tensor(result)
softmax = torch.nn.Softmax()
probs =softmax(result_tensor).numpy()
prob = probs[ind]


print(f'this image with probability {prob*100}%  {label}')