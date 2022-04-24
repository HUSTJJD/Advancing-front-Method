import numpy as np
import matplotlib.pyplot as plt
from Graph import *

np.set_printoptions(threshold=np.inf)


def read_file(file_path, G: Graph, Grid: Graph, grid_type):
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
    # nodes = []
    # faces = []
    adj = [[] for i in range(nnodes)]
    # 边界数量
    frontnum = 0
    for j in face_pos:
        nfaces1 = int(list[j][3], 16) - int(list[j][2], 16) + 1
        if face_pos.index(j) != len(face_pos) - 1:
            frontnum += nfaces1

    # 生成节点对象
    # 节点编号已经处理到 ( 0, n-1 )
    if grid_type:
        pass
    else:
        for i in list[21:21 + nnodes]:
            G.xmin = min(G.xmin, float(i[0]))
            G.xmax = max(G.xmax, float(i[0]))
            G.ymin = min(G.ymin, float(i[1]))
            G.ymax = max(G.ymax, float(i[1]))
            Grid.add_node(Node(-1, float(i[0]), float(i[1])))
        for i in list[21:21 + frontnum]:
            G.add_node(Node(-1, float(i[0]), float(i[1])))

        # 处理 cell / face / adjenct
        for j in face_pos:
            nfaces1 = int(list[j][3], 16) - int(list[j][2], 16) + 1
            bctype = int(list[j][4], 16)
            # if grid_type == 0:
            if face_pos.index(j) != len(face_pos) - 1:
                for i in list[j + 1:j + nfaces1 + 1]:
                    # 单元编号已经处理到 ( 0, n-1 )
                    G.add_front(
                        Face(G.node_list[int(i[0], 16) - 1],
                             G.node_list[int(i[1], 16) - 1], bctype, -1, 0))
            for i in list[j + 1:j + nfaces1 + 1]:
                Grid.add_face(
                    Face(Grid.node_list[int(i[0], 16) - 1],
                         Grid.node_list[int(i[1], 16) - 1], bctype,
                         int(i[2], 16) - 1,
                         int(i[3], 16) - 1))

                # 邻接表
                # if int(i[0], 16) > G.boundarynum | int(i[1], 16) > G.boundarynum:
                #     pass
                # else:
                # adj[int(i[0], 16)-1].append(int(i[1], 16)-1)
                # adj[int(i[1], 16)-1].append(int(i[0], 16)-1)
                # 生成cell列表
                # 表中节点索引已经处理到 ( 0, n-1 )
                if int(i[3], 16) != 0:
                    cells[int(i[2], 16) - 1].append(int(i[0], 16) - 1)
                    cells[int(i[2], 16) - 1].append(int(i[1], 16) - 1)
                    cells[int(i[3], 16) - 1].append(int(i[0], 16) - 1)
                    cells[int(i[3], 16) - 1].append(int(i[1], 16) - 1)

        # elif grid_type == 1:
        #     for i in list[j+1:j+nfaces1+1]:
        #         pass

        for i in range(0, ncells):
            cells[i] = deleteDuplicatedElementFromList3(cells[i])
        for i in range(0, nnodes):
            adj[i] = deleteDuplicatedElementFromList3(adj[i])

        Grid.cell_list = cells
        find_target_nodes(Grid)
        Grid.compute_sp_from_grid()
        G.step_size = Grid.step_size
        # Grid.adjacency_table = adj
        # Grid.cellnum = 0
        # G.front_list = G.face_list
        # G.frontnum = G.facenum
        # G.front_new = G.frontnum


def find_target_nodes(G: Graph):
    # 以左边单元为准找target_point
    for i in G.face_list:
        # print(G.cell_list[i.leftcell][0])
        if (i.node1.id != G.node_list[G.cell_list[i.leftcell][0]].id)\
                & (i.node2.id != G.node_list[G.cell_list[i.leftcell][0]].id):
            i.target_node = G.node_list[G.cell_list[i.leftcell][0]]
        elif (i.node1.id != G.node_list[G.cell_list[i.leftcell][1]].id)\
                & (i.node2.id != G.node_list[G.cell_list[i.leftcell][1]].id):
            i.target_node = G.node_list[G.cell_list[i.leftcell][1]]
        elif (i.node1.id != G.node_list[G.cell_list[i.leftcell][2]].id)\
                & (i.node2.id != G.node_list[G.cell_list[i.leftcell][2]].id):
            i.target_node = G.node_list[G.cell_list[i.leftcell][2]]


def find_refence_nodes(G: Graph):
    subgraph_list = []
    for i in G.face_list:
        neighbors1 = G.adjacency_table[i.node1.id]
        neighbors2 = G.adjacency_table[i.node2.id]
        picked1 = []
        picked2 = []
        for neighbor in neighbors1:
            if neighbor != i.node2.id:
                picked1.append(neighbor)
        for neighbor in neighbors2:
            if neighbor != i.node1.id:
                picked2.append(neighbor)
        for n in picked1:
            for m in picked2:
                # if (n != m) & (n < i.node1.id) & (m < i.node2.id):
                if (n != m):
                    subgraph_list.append(
                        SubGraph(i.node1, i.node2, G.node_list[n],
                                 G.node_list[m], i.target_node))
    G.subgraph_list = subgraph_list


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
    # fig = plt.figure()
    for i in range(0, len(G.subgraph_list), 1000):
        plt.plot([
            G.subgraph_list[i].leftcell.x, G.subgraph_list[i].node1.x,
            G.subgraph_list[i].node2.x, G.subgraph_list[i].rightcell.x
        ], [
            G.subgraph_list[i].leftcell.y, G.subgraph_list[i].node1.y,
            G.subgraph_list[i].node2.y, G.subgraph_list[i].rightcell.y
        ])
        plt.plot(G.subgraph_list[i].target_node.x,
                 G.subgraph_list[i].target_node.y, 'x')
    plt.show()


# 写出训练数据 csv 格式
def write_training_data(G: Graph, sample_file_path):

    f = open(sample_file_path, 'w+')
    print('{:^21}'.format('left_x'),
          '{:^21}'.format('node1_x'),
          '{:^21}'.format('node2_x'),
          '{:^21}'.format('right_x'),
          '{:^21}'.format('left_y'),
          '{:^21}'.format('node1_y'),
          '{:^21}'.format('node2_y'),
          '{:^21}'.format('right_y'),
          '{:^21}'.format('target_x'),
          '{:^21}'.format('target_y'),
          file=f)
    for i in G.subgraph_list:
        print('{:+.18f}'.format((i.leftcell.x - G.xmin) / (G.xmax - G.xmin)),
              '{:+.18f}'.format((i.node1.x - G.xmin) / (G.xmax - G.xmin)),
              '{:+.18f}'.format((i.node2.x - G.xmin) / (G.xmax - G.xmin)),
              '{:+.18f}'.format((i.rightcell.x - G.xmin) / (G.xmax - G.xmin)),
              '{:+.18f}'.format((i.leftcell.y - G.ymin) / (G.ymax - G.ymin)),
              '{:+.18f}'.format((i.node1.y - G.ymin) / (G.ymax - G.ymin)),
              '{:+.18f}'.format((i.node2.y - G.ymin) / (G.ymax - G.ymin)),
              '{:+.18f}'.format((i.rightcell.y - G.ymin) / (G.ymax - G.ymin)),
              '{:+.18f}'.format(
                  (i.target_node.x - G.xmin) / (G.xmax - G.xmin)),
              '{:+.18f}'.format(
                  (i.target_node.y - G.ymin) / (G.ymax - G.ymin)),
              file=f)
    f.close()


# (grid_file_path, sample_file_path)
def data_extration(grid_file_path):
    G = Graph()
    Grid = Graph()
    read_file(grid_file_path, G, Grid, 0)
    find_target_nodes(G)
    find_refence_nodes(G)

    # 观察网格
    # view_grid(G)
    # 观察样本
    view_sample(G)
    # 打印样本
    #write_training_data(G, arg[1])
    return G
