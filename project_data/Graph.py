import math
from re import L
# from codes_AFT.data_extraction import Sp
import matplotlib.pyplot as plt


def deleteDuplicatedElementFromList3(listA):
    return sorted(set(listA), key=listA.index)


class Node:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y
        self.neighbors = []


class Face:
    def __init__(self, node1: Node, node2: Node, boundary_type: int, leftcell: int, rightcell: int):
        self.node1 = node1
        self.node2 = node2
        self.boundary_type = boundary_type
        self.leftcell = leftcell
        self.rightcell = rightcell
        self.distance = math.sqrt(
            math.pow((node1.x - node2.x), 2)+math.pow((node1.y - node2.y), 2))
        self.target_node: Node = None
        self.node1.neighbors.append(self.node2)
        self.node2.neighbors.append(self.node1)
        deleteDuplicatedElementFromList3(self.node1.neighbors)
        deleteDuplicatedElementFromList3(self.node2.neighbors)
        # self.step_size = 1.0*self.distance


class Cell:
    def __init__(self, id: int, node1: Node, node2: Node, node3: Node):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
    #     self.QualityCheck()
    #     self.is_leftcell()

    # def QualityCheck(self):
    #     a = math.sqrt(math.pow((self.node1.x - self.node2.x), 2) +
    #                   math.pow((self.node1.y - self.node2.y), 2))
    #     b = math.sqrt(math.pow((self.node2.x - self.node3.x), 2) +
    #                   math.pow((self.node2.y - self.node3.y), 2))
    #     c = math.sqrt(math.pow((self.node1.x - self.node3.x), 2) +
    #                   math.pow((self.node1.y - self.node3.y), 2))
    #     tmp = (math.pow(a, 2) + math.pow(b, 2)-math.pow(c, 2))/(2.0*a*b)
    #     if abs(tmp-1.0) < 1e-5:
    #         tmp = 1
    #     if abs(tmp+1.0) < 1e-5:
    #         tmp = -1
    #     theta = math.acos(tmp)
    #     area = 0.5*a*b*math.sin(theta) + 1e-40
    #     self.quality = 4.0 * \
    #         math.sqrt(3.0)*area/(math.pow(a, 2)+math.pow(b, 2)+math.pow(c, 2))

    # def is_leftcell(self) -> bool:
    #     x1 = self.node2.x - self.node1.x
    #     y1 = self.node2.y - self.node1.y
    #     x2 = self.node3.x - self.node1.x
    #     y2 = self.node3.y - self.node1.y
    #     res = x1 * y2 - x2 * y1
    #     if(res > 0):
    #         # 是左单元
    #         self.is_not_leftcell = True
    #     else:
    #         self.is_not_leftcell = False


class SubGraph:
    def __init__(self, target_node: Node, node1: Node, node2: Node):
        self.target_node = target_node
        self.node1 = node1
        self.node2 = node2
        self.neighbors = []
        self.x_list = []
        self.y_list = []

    def add_neighbor(self, neighbor: Node):
        self.neighbors.append(neighbor)

    def get_x_list(self):
        if self.y_list == []:
            for i in self.neighbors:
                self.x_list.append(i.x)
        return self.x_list

    def get_y_list(self):
        if self.y_list == []:
            for i in self.neighbors:
                self.y_list.append(i.y)
        return self.y_list

    # def get_x_list_length(self):
    #     return len(self.x_list)

    # def get_y_list_length(self):
    #     return len(self.y_list)


class Graph:
    al = 2.0
    epsilon = 0.6

    def __init__(self):
        self.node_list: Node = []
        self.face_list: Face = []
        self.cell_list: Cell = None
        self.subgraph_list: SubGraph = []
        self.front_list: Face = []
        self.back_grid: Face = []
        self.step_size = []
        self.adjacency_table = [[]]
        self.xmin = 0.0
        self.ymin = 0.0
        self.xmax = 0.0
        self.ymax = 0.0
        self.nodenum = 0
        self.facenum = 0
        self.cellnum = 0
        self.frontnum = 0
        self.boundarynum = 0
        self.maxsubgraph = 0
        self.minsubgraph = 5

    # def add_node(self, node: Node):
    #     node.id = self.nodenum
    #     self.node_list.append(node)
    #     self.nodenum += 1

    # def add_face(self, face: Face):
    #     self.face_list.append(face)
    #     self.facenum += 1

    # def add_cell(self, cell: Cell):
    #     self.cellnum += 1
    #     cell.id = self.cellnum
    #     self.cell_list.append(cell)

    # def add_front(self, front: Face):
    #     self.front_list.append(front)
    #     self.frontnum += 1

    # def remove_front(self, front: Face):
    #     self.front_list.remove(front)
    #     self.frontnum -= 1
    #     pass

    # def remove_cell(self, cell: Cell):
    #     self.cell_list.remove(cell)
    #     self.cellnum -= 1
