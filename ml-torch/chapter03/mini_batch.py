import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from tqdm import *

# hyperparameters
n_samples = 1000
learning_rate = 0.0001
n_epochs = 1000
names = ["Batch", "Stochastic", "Minibatch"]  # 批量梯度下降法、随机梯度下降法、小批量梯度下降法
batch_size = [n_samples, 1, 128]
momentum = [1, 0, 1]
losses = [[], [], []]

# generate data
np.random.seed(0)
x = np.linspace(-5, 5, n_samples)
y = 0.3 * (x ** 2) + np.random.randn(n_samples)
# to Tensor
x = torch.unsqueeze(torch.from_numpy(x).float(), 1)
y = torch.unsqueeze(torch.from_numpy(y).float(), 1)

# dataset
dataset = torch.utils.data.TensorDataset(x, y)


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden1 = nn.Linear(1, 32)
        self.hidden2 = nn.Linear(32, 32)
        self.output = nn.Linear(32, 1)

    def forward(self, x):
        x = torch.relu(self.hidden1(x))
        x = torch.relu(self.hidden2(x))
        return self.output(x)


loss_fn = nn.MSELoss()

# train
for i in range(3):
    model = Model()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum[i])
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size[i], shuffle=True)
    for epoch in tqdm(range(n_epochs), desc=names[i], leave=True, unit=' epoch'):
        x, y = next(iter(dataloader))
        optimizer.zero_grad()
        out = model(x)
        loss = loss_fn(out, y)
        loss.backward()
        optimizer.step()
        losses[i].append(loss.item())

# plot loss
for i, loss_list in enumerate(losses):
    plt.figure(figsize=(12, 4))
    plt.plot(loss_list)
    plt.ylim((0, 15))
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title(names[i])
    plt.savefig(f"output/demo{i}.png")
    plt.show()
