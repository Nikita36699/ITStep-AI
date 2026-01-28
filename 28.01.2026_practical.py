import onnxruntime as ort
import torch
from  PIL import  Image
from torchvision import transforms
import  numpy as np

test_transform = transforms.Compose(
    [transforms.Resize([200, 200]),
    transforms.CenterCrop(180),
    transforms.ToTensor()
    ]
)

class_names =['all', 'hem']

session = ort.InferenceSession('leukemia.onnx')

image = Image.open('data/lesson many/cells/UID_H13_12_4_hem.bmp')

input_tensor: torch.Tensor = test_transform(image)

input_tensor = input_tensor.unsqueeze(0)

#print(input_tensor, input_tensor.shape)

input_tensor = input_tensor.numpy()

# використати моделі
result = session.run(
    output_names=None, #отримати всі вхіднні данні
    input_feed={
        "input": input_tensor
    }
)

print(result)
result  = result[0][0]

#отримати індекс де найбільша ймовірність
ind = result.argmax()

# get class name
label = class_names[ind]

# отримати ймовірність
# max_num = result.max()
# result -= max_num
# exp_result  = np.exp(result)
# probs = exp_result / exp_result.sum()


result_tensor = torch.tensor(result)
softmax = torch.nn.Softmax()
probs =softmax(result_tensor).numpy()
prob = probs[ind]


print(f'this image with probability {prob*100}%  {label}')

 #all hvora hem zdorova



