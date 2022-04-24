import os
import random
from data_extration import data_extration
from multiprocessing.pool import Pool

grid_file_path = './project_data/cas/'
sample_file_path = './project_data/train/'
sample_num = 0
N = 8


# 多线程提取
if __name__ == "__main__":
    pool = Pool()
    args = []

    for a, b, files in os.walk(grid_file_path):
        for filename in files:
            if os.path.splitext(filename)[1] == '.cas':
                c = random.randint(0, 49)
                if c == 25:
                    name = os.path.splitext(filename)[0]
                    grid_path = os.path.join(
                        a, name + '.cas')
                    sample_path = sample_file_path + \
                        a.split('/')[3] + '/' + name + '.csv'
                    arg = (grid_path, sample_path)
                    args.append(arg)
    result = pool.map(data_extration, args)
    print(result)
