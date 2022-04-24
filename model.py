import torch
from torch import nn
from torch.utils.data import Dataset
import numpy as np
import os


class selfDataset(Dataset):
    def __init__(self, sample_path):
        # data = np.zeros((1, 22), dtype=np.float32)
        i = 0
        for a, b, files in os.walk(sample_path):
            for filename in files:
                if os.path.splitext(filename)[1] == '.csv':
                    data = np.loadtxt(sample_path + filename,
                                      dtype=np.float32, delimiter=',', skiprows=1)
                    if i == 0:
                        x_data = data[:, 2:]
                        y_data = data[:, [0, 1]]
                    else:
                        x_data = np.vstack((x_data, data[:, 2:]))
                        y_data = np.vstack((y_data, data[:, [0, 1]]))
                    i += 1
        # LSTM
        # self.create_sequence(x_data)
        # DNN
        # self.x_data = torch.from_numpy(x_data)
        # cnn
        self.create_matrix(x_data)
        self.y_data = torch.from_numpy(y_data)
        self.len = self.y_data.shape[0]

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len

    def create_sequence(self, x, seq_len=2):
        self.x_data = np.zeros((len(x), seq_len, len(x[0])), dtype=np.float32)
        for i in range(0, len(x), 1):
            self.x_data[i] = x[i:i+seq_len]

    def create_matrix(self, x):
        self.x_data = np.zeros((len(x), 1, 10, 2), dtype=np.float32)
        for i in range(0, len(x), 1):
            self.x_data[i] = x[i].reshape((1, 10, 2))


class module(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(module, self).__init__()

        self.model = nn.Sequential(
            # hiden layer的维度要一致
            nn.Linear(input_dim, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            nn.Linear(50, 50),
            nn.ReLU(inplace=True),
            # nn.Dropout(p=0.5),
            nn.Linear(50, output_dim),
        )

    def forward(self, x):
        x = self.model(x)
        return x


class LSTMModel(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_size=56, num_layers=10, dropout=0):
        super(LSTMModel, self).__init__()
        self.model = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout
        )
        self.out = nn.Linear(hidden_size, output_dim)

    def forward(self, x):
        r_out, (h_n, h_c) = self.model(x)
        out = self.out(r_out[:, -1, :])
        return out


class cnnModel(object):
    def __init__(self,):
        super(cnnModel, self).__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=1,
                            out_channels=16,
                            kernel_size=3,
                            stride=2,
                            padding=1),
            torch.nn.BatchNorm2d(16),
            torch.nn.ReLU()
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(16, 32, 3, 2, 1),
            torch.nn.BatchNorm2d(32),
            torch.nn.ReLU()
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(32, 64, 3, 2, 1),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU()
        )
        self.conv4 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 64, 2, 2, 0),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU()
        )
        self.fc1 = torch.nn.Linear(2*2*64, 100)
        self.fc2 = torch.nn.Linear(100, 2)

    def forward(self, x):
        self.conv1(x)
        self.conv2(x)
        self.fc1(x)
        y = self.fc2(x)
        return y
