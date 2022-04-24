from math import pi
from os import sep
from Graph import *
import matplotlib.pyplot as plt
import numpy as np
import random

np.set_printoptions(threshold=np.inf)


def deleteDuplicatedElementFromList3(listA):
    return sorted(set(listA), key=listA.index)


def read_file(file_path, G: Graph, grid_type):
    # 提取文件信息
    with open(file_path, 'r+') as f:
        # 读入文件信息
        all_line = f.readlines()
        list = []
        face_pos = []
        j = 0
        for line in all_line:
            line = line.split(' ')
            for i in range(len(line) - 1, -1, -1):
                if line[i] == '':
                    line.remove('')
            if line[0] == '(13':
                face_pos.append(j)
            list.append(line)
            j += 1
        f.close()
    face_pos.pop(0)
    face_pos.sort(reverse=True)
    # 节点数量
    nnodes = int(list[6][5].rstrip('\")\n'))
    # 阵面数量
    nfaces = int(list[9][6].rstrip('\")\n'))
    # 单元数量
    ncells = int(list[14][6].rstrip('\")\n'))

    # 定义【临时数据】存储
    cells = [[] for i in range(ncells)]
    nodes = []
    faces = []
    adj = [[] for i in range(nnodes)]

    # 生成节点对象
    # 节点编号已经处理到 ( 0, n-1 )
    for i in list[21:21 + nnodes]:
        G.xmin = min(G.xmin, float(i[0]))
        G.xmax = max(G.xmax, float(i[0]))
        G.ymin = min(G.ymin, float(i[1]))
        G.ymax = max(G.ymax, float(i[1]))
        nodes.append(Node(list.index(i) - 21, float(i[0]), float(i[1])))

    # 处理 cell / face / adjenct
    for j in face_pos:
        nfaces1 = int(list[j][3], 16) - int(list[j][2], 16) + 1
        if face_pos.index(j) != len(face_pos) - 1:
            G.boundarynum += nfaces1
        bctype = int(list[j][4], 16)
        if grid_type == 0:
            for i in list[j + 1:j + nfaces1 + 1]:
                # 单元编号已经处理到 ( 0, n-1 )
                faces.append(
                    Face(nodes[int(i[0], 16) - 1], nodes[int(i[1], 16) - 1],
                         bctype, (int(i[2], 16) - 1), (int(i[3], 16) - 1)))
                # 邻接表
                adj[int(i[0], 16) - 1].append(int(i[1], 16) - 1)
                adj[int(i[1], 16) - 1].append(int(i[0], 16) - 1)
                # 生成cell列表
                # 表中节点索引已经处理到 ( 0, n-1 )
                if int(i[3], 16) != 0:
                    cells[int(i[2], 16) - 1].append(int(i[0], 16) - 1)
                    cells[int(i[2], 16) - 1].append(int(i[1], 16) - 1)
                    cells[int(i[3], 16) - 1].append(int(i[0], 16) - 1)
                    cells[int(i[3], 16) - 1].append(int(i[1], 16) - 1)

        elif grid_type == 1:
            for i in list[j + 1:j + nfaces1 + 1]:
                pass
    for i in range(0, ncells):
        cells[i] = deleteDuplicatedElementFromList3(cells[i])
    for i in range(0, nnodes):
        adj[i] = deleteDuplicatedElementFromList3(adj[i])

    G.cell_list = np.array(cells)
    G.face_list = np.array(faces)
    G.node_list = np.array(nodes)
    G.adjacency_table = np.array(adj)
    f = open('./adj.txt', 'w+')
    print(G.adjacency_table, file=f)
    f.close()
    G.nodenum = nnodes
    G.facenum = nfaces
    G.cellnum = ncells


def find_target_nodes(G: Graph):
    # 以左边单元为准找target_point
    for i in G.face_list:
        if (i.node1.id != G.node_list[G.cell_list[i.leftcell, 0]].id)\
                & (i.node2.id != G.node_list[G.cell_list[i.leftcell, 0]].id):
            i.target_node = G.node_list[G.cell_list[i.leftcell, 0]]
        elif (i.node1.id != G.node_list[G.cell_list[i.leftcell, 1]].id)\
                & (i.node2.id != G.node_list[G.cell_list[i.leftcell, 1]].id):
            i.target_node = G.node_list[G.cell_list[i.leftcell, 1]]
        elif (i.node1.id != G.node_list[G.cell_list[i.leftcell, 2]].id)\
                & (i.node2.id != G.node_list[G.cell_list[i.leftcell, 2]].id):
            i.target_node = G.node_list[G.cell_list[i.leftcell, 2]]


def find_refence_nodes(G: Graph):
    subgraph_list = []
    for i in G.face_list:
        if i.boundary_type == 3:
            pass
        else:
            neighbors1 = G.adjacency_table[i.node1.id]
            neighbors2 = G.adjacency_table[i.node2.id]
            picked = neighbors1 + neighbors2
            picked = deleteDuplicatedElementFromList3(picked)
            picked.remove(i.node1.id)
            picked.remove(i.node2.id)
            # 不要删除目标点 更容易拟合？
            # picked.remove(i.target_node.id)
            if len(picked) > G.maxsubgraph:
                G.maxsubgraph = len(picked)
            if len(picked) < G.minsubgraph:
                G.minsubgraph = len(picked)
            maxn = 8
            if len(picked) < maxn:
                maxn = len(picked)
            minn = 4
            if len(picked) < minn:
                minn = len(picked)
            n = random.randint(minn, maxn)
            picked = random.sample(picked, n)
            temp = SubGraph(i.target_node, i.node1, i.node2)
            for j in picked:
                temp.add_neighbor(G.node_list[j])
            subgraph_list.append(temp)
    G.subgraph_list = np.array(subgraph_list)


def view_grid(G: Graph):
    fig = plt.figure()
    for i in G.face_list:
        if i.boundary_type == 2:
            plt.plot([i.node1.x, i.node2.x], [i.node1.y, i.node2.y], color='r')
        if i.boundary_type == 3:
            plt.plot([i.node1.x, i.node2.x], [i.node1.y, i.node2.y], color='b')
        if i.boundary_type == 9:
            plt.plot([i.node1.x, i.node2.x], [i.node1.y, i.node2.y], color='y')
    plt.show()


def view_sample(G: Graph):
    fig = plt.figure()
    for i in range(0, len(G.subgraph_list), 500):
        plt.plot(G.subgraph_list[i].get_x_list(),
                 G.subgraph_list[i].get_y_list(), 'o--')
        plt.plot(G.subgraph_list[i].target_node.x,
                 G.subgraph_list[i].target_node.y, 'x')
    plt.show()


# 写出训练数据 csv 格式
def write_training_data(G: Graph, sample_file_path):

    f = open(sample_file_path, 'w+')
    print('{:^21}'.format('target_x'),
          '{:^21}'.format('target_y'),
          '{:^21}'.format('node1_x'),
          '{:^21}'.format('node1_y'),
          '{:^21}'.format('node2_x'),
          '{:^21}'.format('node2_y'),
          file=f,
          sep=',')
    for i in G.subgraph_list:
        temp_x = []
        temp_y = []
        # 先缩放后旋转再平移
        dist = math.sqrt(
            math.pow(i.node1.x - i.node2.x, 2) +
            math.pow(i.node1.y - i.node2.y, 2))
        ab = [(i.node2.x - i.node1.x) / dist, (i.node2.y - i.node1.y) / dist]
        rotate_angle = math.acos(ab[0]) if (ab[1] < 0) else -math.acos(ab[0])
        scale = 1. / dist

        # print(
        #     '{:+.18f}'.format(i.target_node.x - x_offset),
        #     '{:+.18f}'.format(i.target_node.y - y_offset),
        #     '{:+.18f}'.format(i.node1.x - x_offset),
        #     '{:+.18f}'.format(i.node1.y - y_offset),
        #     '{:+.18f}'.format(i.node2.x - x_offset),
        #     '{:+.18f}'.format(i.node2.y - y_offset),
        # file=f, end=',', sep=',')
        temp_x.append(i.target_node.x)
        temp_y.append(i.target_node.y)
        temp_x.append(i.node1.x)
        temp_y.append(i.node1.y)
        temp_x.append(i.node2.x)
        temp_y.append(i.node2.y)
        temp_x += i.get_x_list()
        temp_y += i.get_y_list()
        # plt.plot(temp_x, temp_y, 'ro')
        # 平移
        x_offset = temp_x[1]
        y_offset = temp_y[1]
        for j in range(0, len(temp_x)):
            temp_x[j] = temp_x[j] - x_offset
            temp_y[j] = temp_y[j] - y_offset

        # 旋转
        for j in range(0, len(temp_x)):
            x_pre = temp_x[j]
            y_pre = temp_y[j]
            temp_x[j] = x_pre * \
                math.cos(rotate_angle) - y_pre * math.sin(rotate_angle)
            temp_y[j] = y_pre * \
                math.cos(rotate_angle) + x_pre * math.sin(rotate_angle)

        # 缩放
        for j in range(0, len(temp_x)):
            temp_x[j] = temp_x[j] * scale
            temp_y[j] = temp_y[j] * scale

        # 平移
        x_offset = temp_x[1] - 1.0
        y_offset = temp_y[1] - 1.0
        for j in range(0, len(temp_x)):
            temp_x[j] = temp_x[j] - x_offset
            temp_y[j] = temp_y[j] - y_offset

        # zero padding
        if len(temp_x) < 11:
            for m in range(0, 11 - len(temp_x)):
                temp_x.append(0.0)
                temp_y.append(0.0)
        print('{:+.18f}'.format(temp_x[0]), file=f, end=',')
        print('{:+.18f}'.format(temp_y[0]), file=f, end=',')
        for j in range(1, len(temp_x)):
            print('{:+.18f}'.format(temp_x[j]), file=f, end=',')
        for j in range(1, len(temp_x)):
            if j == len(temp_y) - 1:
                print('{:+.18f}'.format(temp_y[j]), file=f)
            else:
                print('{:+.18f}'.format(temp_y[j]), file=f, end=',')
        # print(
        #     '{:+.18f}'.format((i.target_node.x-G.xmin)/(G.xmax-G.xmin)),
        #     '{:+.18f}'.format((i.target_node.y-G.ymin)/(G.ymax-G.ymin)),
        #     '{:+.18f}'.format((i.node1.x - G.xmin) / (G.xmax-G.xmin)),
        #     '{:+.18f}'.format((i.node1.y - G.ymin) / (G.ymax-G.ymin)),
        #     '{:+.18f}'.format((i.node2.x - G.xmin) / (G.xmax-G.xmin)),
        #     '{:+.18f}'.format((i.node2.y - G.ymin) / (G.ymax-G.ymin)),
        #     file=f, end=',', sep=',')
        # temp_x = i.get_x_list()
        # temp_y = i.get_y_list()
        # if len(temp_x) < 8:
        #     for m in range(0, 8-len(temp_x)):
        #         temp_x.append(G.xmin)
        #         temp_y.append(G.ymin)
        # for j in range(0, len(temp_x)):
        #     print(
        #         '{:+.18f}'.format((temp_x[j] -
        #                           G.xmin) / (G.xmax-G.xmin)), file=f, end=',')
        #     if j == len(temp_y)-1:
        #         print(
        #             '{:+.18f}'.format((temp_y[j] -
        #                                G.ymin) / (G.ymax-G.ymin)), file=f)
        #     else:
        #         print(
        #             '{:+.18f}'.format((temp_y[j] -
        #                                G.ymin) / (G.ymax-G.ymin)), file=f, end=',')
    f.close()


# (grid_file_path, sample_file_path)
def data_extration(arg):
    G = Graph()

    read_file(arg[0], G, 0)
    find_target_nodes(G)
    find_refence_nodes(G)

    # 观察网格
    # view_grid(G)
    # 观察样本
    view_sample(G)
    # 打印样本
    # write_training_data(G, arg[1])
    # print(G.maxsubgraph)
    # print(G.minsubgraph)
    return (len(G.subgraph_list))


if __name__ == '__main__':
    data_extration(('./project_data/cas/in-100-out-50-front/a18/a18.cas',
                    './project_data/train/in-100-out-50-front/a18.csv'))
