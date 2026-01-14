def f(x):
  return x**2/3 + torch.sin(torch.pi*x)

y_true = 1



import torch
from torch.optim import SGD

x = torch.tensor(3.5, requires_grad=True)

optimizer = SGD(params=[x], lr=0.01)

for t in range(1000):
    nn_result = f(x)

    error = y_true - nn_result

    error.backward()

    optimizer.step()

    optimizer.zero_grad()


