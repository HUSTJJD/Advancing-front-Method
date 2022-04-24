import math
from re import L
# from codes_AFT.data_extraction import Sp
import matplotlib.pyplot as plt
import time


def deleteDuplicatedElementFromList3(listA):
    return sorted(set(listA), key=listA.index)


class Node:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y
        self.neighbors = []

    # def == (self, other):


class Face:
    def __init__(self, node1: Node, node2: Node, boundary_type: int,
                 leftcell: int, rightcell: int):
        self.node1 = node1
        self.node2 = node2
        self.boundary_type = boundary_type
        self.leftcell = leftcell
        self.rightcell = rightcell
        self.distance = math.sqrt(
            math.pow((node1.x - node2.x), 2) +
            math.pow((node1.y - node2.y), 2))
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
        self.QualityCheck()
        self.is_leftcell()

    def QualityCheck(self):
        a = math.sqrt(
            math.pow((self.node1.x - self.node2.x), 2) +
            math.pow((self.node1.y - self.node2.y), 2))
        b = math.sqrt(
            math.pow((self.node2.x - self.node3.x), 2) +
            math.pow((self.node2.y - self.node3.y), 2))
        c = math.sqrt(
            math.pow((self.node1.x - self.node3.x), 2) +
            math.pow((self.node1.y - self.node3.y), 2))
        tmp = (math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / (2.0 * a *
                                                                    b)
        if abs(tmp - 1.0) < 1e-5:
            tmp = 1
        if abs(tmp + 1.0) < 1e-5:
            tmp = -1
        theta = math.acos(tmp)
        area = 0.5 * a * b * math.sin(theta) + 1e-40
        self.quality = 4.0 * \
            math.sqrt(3.0)*area/(math.pow(a, 2)+math.pow(b, 2)+math.pow(c, 2))

    def is_leftcell(self) -> bool:
        x1 = self.node2.x - self.node1.x
        y1 = self.node2.y - self.node1.y
        x2 = self.node3.x - self.node1.x
        y2 = self.node3.y - self.node1.y
        res = x1 * y2 - x2 * y1
        if (res > 0):
            # 是左单元
            self.is_not_leftcell = True
        else:
            self.is_not_leftcell = False


class SubGraph:
    def __init__(self, node1: Node, node2: Node, leftcell: Node,
                 rightcell: Node, target_node: Node):
        self.node1 = node1
        self.node2 = node2
        self.leftcell = leftcell
        self.rightcell = rightcell
        self.target_node = target_node


class Graph:
    al = 3.0
    epsilon = 0.9
    coeff = 0.8

    def __init__(self):
        self.node_list: Node = []
        self.face_list: Face = []
        self.cell_list: Cell = []
        # self.subgraph_list: SubGraph = []
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
        # self.face_new = 0
        self.front_new = 0

    def add_node(self, node: Node):
        node.id = self.nodenum
        self.node_list.append(node)
        self.nodenum += 1

    def add_face(self, face: Face):
        self.face_list.append(face)
        self.facenum += 1
        # self.face_new += 1

    def add_cell(self, cell: Cell):
        self.cellnum += 1
        cell.id = self.cellnum
        self.cell_list.append(cell)

    def add_front(self, front: Face):
        self.front_list.append(front)
        self.frontnum += 1
        self.front_new += 1

    def remove_front(self, front: Face):
        self.front_list.remove(front)
        self.frontnum -= 1
        pass

    def remove_cell(self, cell: Cell):
        self.cell_list.remove(cell)
        self.cellnum -= 1

    def AFt_meshing(self):
        self.sort_front()
        # 当阵面不空
        t_start = time.time()
        while self.frontnum > 0:
            # 取出阵面生成单元
            print('还剩' + str(self.frontnum) + '个')
            selected_node = self.generate_tri(self.front_list[0])
            if selected_node != None:
                self.update_tri_cells(self.front_list[0], selected_node)
                # self.view_graph()
                self.remove_inactive_front()
                # if self.frontnum % 300 == 0:
                #     self.sort_front()
                self.al = 3.0
            else:
                self.al = self.al * 1.2
                continue
        # plt.savefig('./result2.jpg', dpi=3600, format='eps')
        t_end = time.time()
        t = t_end - t_start
        print('time cost: ' + str(t))
        print('node num: ' + str(self.nodenum))
        print('face num: ' + str(self.facenum))
        print('cell num: ' + str(self.cellnum))
        self.view_result()

    def sort_front(self):
        self.front_list = sorted(self.front_list,
                                 key=lambda x: x.distance,
                                 reverse=False)

    def generate_tri(self, face: Face):
        new_node, sp = self.new_point_tri(face)
        candidate_node_front = self.find_candidate_node_front(
            new_node, sp, face)
        if len(candidate_node_front) != 0:
            candidate_node_front = deleteDuplicatedElementFromList3(
                candidate_node_front)
            # if face.node1 in candidate_node_front:
            #     candidate_node_front.remove(face.node1)
            # if face.node2 in candidate_node_front:
            #     candidate_node_front.remove(face.node2)
            candidate_front = self.find_candidate_front(candidate_node_front)
            candidate_front = deleteDuplicatedElementFromList3(candidate_front)

        candidate_node_face = self.find_candidate_node_face(new_node, sp, face)
        candidate_node_face += candidate_node_front
        candidate_face = []
        if len(candidate_node_face) != 0:
            candidate_node_face = deleteDuplicatedElementFromList3(
                candidate_node_face)
            # if face.node1 in candidate_node_face:
            #     candidate_node_face.remove(face.node1)
            # if face.node2 in candidate_node_face:
            #     candidate_node_face.remove(face.node2)
            candidate_face = self.find_candidate_face(candidate_node_face)
            candidate_face = deleteDuplicatedElementFromList3(candidate_face)

        candidate_cell = self.quality_check_tri(face, candidate_node_front)
        selected_cell = None
        for i in candidate_cell:
            flag = 0
            for j in candidate_front:
                if self.is_not_cross(i.node1, i.node3, j.node1, j.node2) == 1:
                    # print('node1-new_node / candidate_face 相交')
                    flag = 1
                    break
                elif self.is_not_cross(i.node2, i.node3, j.node1,
                                       j.node2) == 1:
                    # print('node2-new_node / candidate_face 相交')
                    flag = 1
                    break
            if flag == 1:
                continue
            for j in candidate_face:
                if self.is_not_cross(i.node1, i.node3, j.node1, j.node2) == 1:
                    flag = 1
                    break
                elif self.is_not_cross(i.node2, i.node3, j.node1,
                                       j.node2) == 1:
                    flag = 1
                    break
                elif ((i.node1 == j.node1) | (i.node2 == j.node1) | (i.node3 == j.node1)) \
                        & ((i.node1 == j.node2) | (i.node2 == j.node2) | (i.node3 == j.node2)):
                    flag = 1
                    break
            if flag == 1:
                continue
            if i.is_not_leftcell:
                selected_cell = i
                break
            else:
                continue
        if selected_cell != None:
            if selected_cell.node3.id == -1:
                self.add_node(selected_cell.node3)
            return selected_cell.node3
        else:
            return None

    def new_point_tri(self, face: Face):
        sp = face.distance * 0.866
        if face.boundary_type == 3:
            sp = face.distance * math.sqrt(3.0) / 2.0
        normal_vector = [
            -(face.node2.y - face.node1.y) / (face.distance + 1e-40),
            (face.node2.x - face.node1.x) / (face.distance + 1e-40)
        ]
        x = (face.node1.x + face.node2.x) / 2.0 + normal_vector[0] * sp
        y = (face.node1.y + face.node2.y) / 2.0 + normal_vector[1] * sp
        new_node = Node(id=-1, x=x, y=y)
        return new_node, sp

    # 寻找候选点
    def find_candidate_node_front(self, new_node: Node, sp: float, face: Face):
        candidate = [
            new_node,
        ]
        radius = self.al * sp
        for i in self.front_list:
            distance1 = pow(i.node1.x-new_node.x, 2) + \
                pow(i.node1.y-new_node.y, 2)
            distance2 = pow(i.node2.x-new_node.x, 2) + \
                pow(i.node2.y-new_node.y, 2)
            if (distance1 < pow(radius, 2)) & (i.node1 != face.node1) & (
                    i.node1 != face.node2):
                candidate.append(i.node1)
            if (distance2 < pow(radius, 2)) & (i.node2 != face.node1) & (
                    i.node2 != face.node2):
                candidate.append(i.node2)
            if (i.node2 == face.node1) & (i.node1 != face.node2)\
                    or ((i.node2 == face.node2) & (i.node1 != face.node1)):
                candidate.append(i.node1)
            if (i.node1 == face.node2) & (i.node2 != face.node1)\
                    or ((i.node1 == face.node1) & (i.node2 != face.node2)):
                candidate.append(i.node2)
        return candidate

    def find_candidate_node_face(self, new_node: Node, sp: float, face: Face):
        candidate = []
        radius = self.al * sp
        if self.facenum != 0:
            for i in self.face_list:
                distance1 = pow(i.node1.x-new_node.x, 2) + \
                    pow(i.node1.y-new_node.y, 2)
                distance2 = pow(i.node2.x-new_node.x, 2) + \
                    pow(i.node2.y-new_node.y, 2)
                if (distance1 < pow(radius, 2)) & (i.node1 != face.node1) & (
                        i.node1 != face.node2):
                    candidate.append(i.node1)
                if (distance2 < pow(radius, 2)) & (i.node1 != face.node1) & (
                        i.node1 != face.node2):
                    candidate.append(i.node2)
            if (i.node2 == face.node1) & (i.node1 != face.node2)\
                    or ((i.node2 == face.node2) & (i.node1 != face.node1)):
                candidate.append(i.node2)
            if (i.node1 == face.node2) & (i.node2 != face.node1)\
                    or ((i.node1 == face.node1) & (i.node2 != face.node2)):
                candidate.append(i.node2)
        return candidate

    # 查询临近阵面 进行相交性判断
    def find_candidate_front(self, candidate_node: Node):
        candidate = []
        for i in self.front_list:
            if (i.node1 in candidate_node) or (i.node2 in candidate_node):
                candidate.append(i)
        return candidate

    def find_candidate_face(self, candidate_node: Node):
        candidate = []
        for i in self.face_list:
            if (i.node1 in candidate_node) or (i.node2 in candidate_node):
                candidate.append(i)
        return candidate

    # 相交性判断 已检查
    def is_not_cross(self, a: Node, b: Node, c: Node, d: Node) -> bool:
        if ((min(a.x, b.x) <= max(c.x, d.x))
                and (min(c.x, d.x) <= max(a.x, b.x))
                and (min(a.y, b.y) <= max(c.y, d.y))
                and (min(c.y, d.y) <= max(a.y, b.y))):
            u = (c.x - a.x) * (b.y - a.y) - (b.x - a.x) * (c.y - a.y)
            v = (d.x - a.x) * (b.y - a.y) - (b.x - a.x) * (d.y - a.y)
            w = (a.x - c.x) * (d.y - c.y) - (d.x - c.x) * (a.y - c.y)
            z = (b.x - c.x) * (d.y - c.y) - (d.x - c.x) * (b.y - c.y)
            eps = 1e-9
            if (u * v <= 0) and (w * z <= 0):
                if (((abs(a.x - c.x) < eps) & (abs(a.x - c.x) < eps))
                        | ((abs(a.x - d.x) < eps) & (abs(a.x - d.x) < eps))
                        | ((abs(b.x - c.x) < eps) & (abs(b.x - c.x) < eps))
                        | ((abs(b.x - d.x) < eps) & (abs(b.x - d.x) < eps))):
                    return 0
                else:
                    return 1
            return 0
        return 0

    # 删除非活跃阵面
    def remove_inactive_front(self):
        for i in self.front_list[::-1]:
            if (i.leftcell != -1) & (i.rightcell != -1):
                self.remove_front(i)
                # print('删除阵面' + str(i.node1.x) + ' ' + str(i.node1.y) +
                #       ' , ' + str(i.node2.x) + ' ' + str(i.node2.y))
                self.add_face(i)

    def quality_check_tri(self, face: Face, candidate_node: Node):
        candidate_cell = []
        for i in candidate_node:
            temp_cell = Cell(-1, face.node1, face.node2, i)
            if i.id == -1:
                temp_cell.quality *= self.coeff
            candidate_cell.append(temp_cell)
        candidate_cell = sorted(candidate_cell,
                                key=lambda x: x.quality,
                                reverse=True)
        return candidate_cell

    def update_tri_cells(self, face: Face, selected_node: Node):
        self.update_AFT_info_tri(face, selected_node)
        neighbors = []
        temp_cell = []
        if selected_node.id != self.nodenum:
            neighbors = []
            for i in self.front_list:
                if i.node1 == selected_node and i.node2.id != -1:
                    neighbors.append(i.node2)
                elif i.node2 == selected_node and i.node2.id != -1:
                    neighbors.append(i.node1)
            neighbors = deleteDuplicatedElementFromList3(neighbors)
            for i in neighbors:
                for j in self.front_list:
                    if i == j.node1:
                        if j.node2 in neighbors:
                            temp = [selected_node, i, j.node2]
                            # temp = sorted(temp, key=lambda x: x.x)
                            temp_cell.append(temp)
                        pass
                    if i == j.node2:
                        if j.node1 in neighbors:
                            temp = [selected_node, i, j.node1]
                            # temp = sorted(temp, key=lambda x: x.x)
                            temp_cell.append(temp)

            # 去掉重复的
            for i in range(0, len(temp_cell)):
                for j in range(len(temp_cell) - 1, i, -1):
                    if sorted(temp_cell[i],
                              key=lambda x: x.x) == sorted(temp_cell[j],
                                                           key=lambda x: x.x):
                        temp_cell.remove(temp_cell[j])

            # 去掉已有的 可能有问题
            for i in range(len(temp_cell) - 1, -1, -1):
                # nodes = [temp_cell[i].node1,
                #          temp_cell[i].node2, temp_cell[i].node3]
                for j in self.cell_list:
                    if (j.node1 in temp_cell[i]) and (
                            j.node2 in temp_cell[i]) and (j.node3
                                                          in temp_cell[i]):
                        temp_cell.remove(temp_cell[i])
            # 去掉质量不好的单元
            for i in range(len(temp_cell) - 1, -1, -1):
                if Cell(-1, temp_cell[i][0], temp_cell[i][1],
                        temp_cell[i][2]).quality < self.epsilon:
                    temp_cell.remove(temp_cell[i])
            # 更新单元
            for i in temp_cell:
                self.cellnum += 1
                self.update_AFT_info_general_tri(i)

    def update_AFT_info_general_tri(self, temp_cell):
        flag1 = Cell(-1, temp_cell[0], temp_cell[1],
                     temp_cell[2]).is_not_leftcell
        exist_face, direction = self.front_exist(temp_cell[0], temp_cell[1])
        if flag1:
            if exist_face != None:
                if direction == 1:
                    exist_face.leftcell = self.cellnum
                elif direction == -1:
                    exist_face.rightcell = self.cellnum
            else:
                f = Face(temp_cell[1], temp_cell[0], 1, -1, self.cellnum)
                self.add_front(f)
                # self.add_face(f)
        else:
            if exist_face != None:
                if direction == 1:
                    exist_face.rightcell = self.cellnum
                elif direction == -1:
                    exist_face.leftcell = self.cellnum
            else:
                f = Face(temp_cell[1], temp_cell[0], 1, self.cellnum, -1)
                self.add_front(f)
                # self.add_face(f)

        flag2 = Cell(-1, temp_cell[1], temp_cell[2],
                     temp_cell[0]).is_not_leftcell
        exist_face, direction = self.front_exist(temp_cell[1], temp_cell[2])
        if flag2:
            if exist_face != None:
                if direction == 1:
                    exist_face.leftcell = self.cellnum
                elif direction == -1:
                    exist_face.rightcell = self.cellnum
            else:
                f = Face(temp_cell[2], temp_cell[1], 1, -1, self.cellnum)
                self.add_front(f)
                # self.add_face(f)
        else:
            if exist_face != None:
                if direction == 1:
                    exist_face.rightcell = self.cellnum
                elif direction == -1:
                    exist_face.leftcell = self.cellnum
            else:
                f = Face(temp_cell[2], temp_cell[1], 1, self.cellnum, -1)
                self.add_front(f)
                # self.add_face(f)

        flag3 = Cell(-1, temp_cell[2], temp_cell[0],
                     temp_cell[1]).is_not_leftcell
        exist_face, direction = self.front_exist(temp_cell[2], temp_cell[0])
        if flag3:
            if exist_face != None:
                if direction == 1:
                    exist_face.leftcell = self.cellnum
                elif direction == -1:
                    exist_face.rightcell = self.cellnum
            else:
                f = Face(temp_cell[0], temp_cell[2], 1, -1, self.cellnum)
                self.add_front(f)
                # self.add_face(f)
        else:
            if exist_face != None:
                if direction == 1:
                    exist_face.rightcell = self.cellnum
                elif direction == -1:
                    exist_face.leftcell = self.cellnum
            else:
                f = Face(temp_cell[0], temp_cell[2], 1, self.cellnum, -1)
                self.add_front(f)
                # self.add_face(f)

    def update_AFT_info_tri(self, face: Face, selected_node: Node):
        flag1 = Cell(-1, face.node1, face.node2, selected_node).is_not_leftcell
        if flag1:
            face.leftcell = self.cellnum
        else:
            face.rightcell = self.cellnum

        flag2 = Cell(-1, selected_node, face.node1, face.node2).is_not_leftcell
        exist_face, direction = self.front_exist(selected_node, face.node1)
        if flag2:
            if exist_face != None:
                if direction == 1:
                    exist_face.leftcell = self.cellnum
                elif direction == -1:
                    exist_face.rightcell = self.cellnum
            else:
                f = Face(face.node1, selected_node, 1, -1, self.cellnum)
                self.add_front(f)
                # self.add_face(f)
        else:
            if exist_face != None:
                if direction == 1:
                    exist_face.rightcell = self.cellnum
                elif direction == -1:
                    exist_face.leftcell = self.cellnum
            else:
                f = Face(face.node1, selected_node, 1, self.cellnum, -1)
                self.add_front(f)
                # self.add_face(f)

        flag3 = Cell(-1, face.node2, selected_node, face.node1).is_not_leftcell
        exist_face, direction = self.front_exist(face.node2, selected_node)
        if flag3:
            if exist_face != None:
                if direction == 1:
                    exist_face.leftcell = self.cellnum
                elif direction == -1:
                    exist_face.rightcell = self.cellnum
            else:
                f = Face(selected_node, face.node2, 1, -1, self.cellnum)
                self.add_front(f)
                # self.add_face(f)
        else:
            if exist_face != None:
                if direction == 1:
                    exist_face.rightcell = self.cellnum
                elif direction == -1:
                    exist_face.leftcell = self.cellnum
            else:
                f = Face(selected_node, face.node1, 1, self.cellnum, -1)
                self.add_front(f)
                # self.add_face(f)

    # checked
    def front_exist(self, node1: Node, node2: Node):
        exist_face = None
        direction = 0
        for i in self.front_list:
            if (i.node1 == node1) & (i.node2 == node2):
                exist_face = i
                direction = 1
                break
            elif (i.node2 == node1) & (i.node1 == node2):
                exist_face = i
                direction = -1
                break
        return exist_face, direction

    # 查看网格 checked
    def view_graph(self):
        # if self.facenum != 0:
        #     for i in range(self.facenum - 1, self.facenum - self.face_new - 1, -1):
        #         plt.plot([self.face_list[i].node1.x, self.face_list[i].node2.x],
        #                  [self.face_list[i].node1.y, self.face_list[i].node2.y])
        #         self.face_new = 0
        if self.frontnum != 0:
            for i in range(self.frontnum - 1,
                           self.frontnum - self.front_new - 1, -1):
                plt.plot(
                    [self.front_list[i].node1.x, self.front_list[i].node2.x],
                    [self.front_list[i].node1.y, self.front_list[i].node2.y],
                    linewidth=0.01)
            self.front_new = 0
        # plt.pause(0.001)

    def view_result(self):
        for i in self.face_list:
            plt.plot([self.front_list[i].node1.x, self.front_list[i].node2.x],
                     [self.front_list[i].node1.y, self.front_list[i].node2.y],
                     linewidth=0.6)
            plt.pause(0.0001)

    def compute_sp_from_grid(self):
        for i in self.face_list:
            normal_vector = [
                -(i.node2.y - i.node1.y) / (i.distance + 1e-40),
                (i.node2.x - i.node1.x) / (i.distance + 1e-40)
            ]
            v_ac = [i.target_node.x - i.node1.x, i.target_node.y - i.node1.y]
            step_size = v_ac[0] * normal_vector[0] + v_ac[1] * normal_vector[1]
            self.step_size.append(step_size)
