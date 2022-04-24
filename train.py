import torch
from torch import nn
import numpy as np
from torch.cuda.random import seed
from model import LSTMModel, selfDataset, module
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


np.set_printoptions(precision=48, threshold=np.inf)

torch.backends.cudnn.banchmark = False
torch.backends.cudnn.deterministic = True
sample_path = './project_data/train/in-100-out-50-front/'

model_save_path = './'
batch_size = 30
learning_rate = 0.001
epochs = 100
input_dim = 20
output_dim = 2
device = torch.device(
    'cuda') if torch.cuda.is_available() else torch.device('cpu')
# seed = 99
# torch.manual_seed(seed)
# torch.cuda.manual_seed(seed)


dataset = selfDataset(sample_path)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(
    dataset, [train_size, test_size])
# train_dataset, test_dataset = selfDataset(test_path)
train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=4)
test_loader = DataLoader(
    dataset=test_dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=4)


plt.ion()
# net = module(input_dim, output_dim).to(device)
net = LSTMModel(input_dim, output_dim).to(device)


optimizer = torch.optim.Adam(
    net.parameters(), lr=learning_rate, betas=(0.9, 0.99))
criterion = nn.MSELoss().to(device)
train_loss_his = []
test_loss_his = []
net_path = './models/net1'
his_loss_path = './models/his_loss1.txt'
try:
    net.load_state_dict(torch.load(net_path))
except Exception as e:
    print('Error loading')
min_loss_his = 10
try:
    f = open(his_loss_path, 'r+')
    min_loss_his = float(f.read())
    f.close()
except IOError:
    print('Error reading')

for epoch in range(epochs):
    net.train()
    train_loss = 0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        y_pred = net(data)

        loss = criterion(y_pred, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if batch_idx % 700 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.10f}'.format(
                epoch,
                batch_idx * len(data),
                len(train_loader.dataset),
                100. * batch_idx / len(train_loader),
                loss.item()
            ))
        train_loss += loss
    train_loss *= batch_size
    train_loss /= len(train_loader.dataset)
    train_loss_his.append(train_loss.cpu().detach().numpy())
    test_loss = 0
    correct = 0
    net.eval()
    with torch.no_grad():
        for batch_idx, (data, target) in enumerate(test_loader):
            data, target = data.to(device), target.to(device)
            y_pred = net.forward(data)
            loss = criterion(y_pred, target)
            # pred = y_pred.data.max(1)[1]
            correct += y_pred.eq(target.data).sum()
            test_loss += loss
        test_loss *= batch_size
        test_loss /= len(test_loader.dataset)
        test_loss_his.append(test_loss.cpu().detach().numpy())
        if test_loss < min_loss_his:
            min_loss_his = test_loss
            torch.save(obj=net.state_dict(), f=net_path)
            f = open(his_loss_path, 'w')
            print(min_loss_his.item(), file=f)
            f.close()
        print('\nTest set: Average loss : {:.10f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss,
            correct,
            len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))

    plt.plot(train_loss_his, 'r', label='train')
    plt.plot(test_loss_his, 'b', label='tset')
    plt.pause(0.1)
