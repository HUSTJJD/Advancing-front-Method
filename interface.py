import torch
from model import module

net = module(20, 2)
net.load_state_dict(torch.load('./models/net'))
net.eval()
torch.no_grad()


def prediction(ref: list):
    if len(ref) < 20:
        print('错误的输入')
    ref = torch.Tensor(ref)
    x, y = net(ref)
    print(x.item())
    print(y.item())
    return x.item(), y.item()


if __name__ == '__main__':
    ref = [1.000000000000000,
           1.000000000000000,
           2.000000000000000,
           1.000000000000000,
           0.053753945946616,
           1.323447685396621,
           1.500000000000000,
           0.133974596215561,
           0.246763060624557,
           0.342250721657297,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0]
    prediction(ref)
