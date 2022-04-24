import torch
import random
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

np.set_printoptions(precision=48, threshold=np.inf)


class Pipeline(object):
    def __init__(self, **params):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.__init_environment(params['random_state'])
        self.__build_model(**params['model'])
        self.__build_components(**params['hyper'])
        return

    def __init_environment(self, random_state):
        """初始化环境
            Input:
            ------
            random_state: int, 随机种子
        """
        random.seed(random_state)
        np.random.seed(random_state)
        torch.manual_seed(random_state)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

        return

    def __build_model(self, **model_params):
        """加载模型

            Input:
            ------
            model_params: dict, 模型相关参数

        """

        # 加载模型
        self.model = Model(**model_params)
        self.model.to(self.device)

        return
