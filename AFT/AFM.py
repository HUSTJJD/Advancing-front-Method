from numpy.core.shape_base import stack
from Graph import *
# from Queue import Queue, LifoQueue, PriorityQueue
from data_extration import data_extration, view_grid
import matplotlib.pyplot as plt


grid_file_path = "./project_data/cas/in-100-out-50-front/2032c/2032c.cas"
# grid_file_path = "./project_data/cas/0test.cas"
gridType = 0
# 0-单一单元网格，1-混合单元网格
Sp = 1
# 网格步长 % Sp = sqrt(3.0)/2.0
# 0.866，传统阵面推进才需要
al = 2.0
# 在几倍范围内搜索
coeff = 0.8
# 尽量选择现有点的参数，Pbest质量参数的系数
outGridType = 0
# 0-各向同性网格，1-各向异性网格
dt = 0.00001
# 暂停时长
stencilType = 'all'
# 在ANN生成点时，如何取当前阵面的引导点模板，可以随机取1个，或者所有可能都取，最后平均
epsilon = 0.6
# 四边形网格质量要求, 值越大要求越高
# nn_fun = @net_cylinder_quad3
# # net_naca0012_quad
# net_airfoil_hybrid
# net_cylinder_quad3
num_label = 0
# flag_label = zeros(1, 10000)99
cellNodeTopo = []
SpDefined = 1
# 0-未定义步长，直接采用网格点；1-定义了步长文件；2-ANN输出了步长


# AFT_stack = []
G = Graph()
if __name__ == '__main__':
    # 读取边界
    G = data_extration(grid_file_path)
    # AFT_stack = G.face_list
    # G.AFT_stack = G.face_list
    plt.ion()
    plt.figure(1)
    G.AFt_meshing()
    # 阵面排序
