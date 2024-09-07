import tkinter as tk
import math
import time


class Digraph:
    def __init__(self, num):
        self.num_vertices = num
        self.num_edges = 0
        self.adj_list = [[] for _ in range(num)]

    def add_edge(self, x, y, weight):
        """加入顶点x 到 顶点y的带权边"""
        if x >= self.num_vertices or y >= self.num_vertices or x == y:
            return False
        else:
            self.adj_list[x].append((y, weight))
            self.num_edges += 1
            return True

    def remove_edge(self, x, y):
        """删除顶点x 到 顶点y的边"""
        if x >= self.num_vertices or y >= self.num_vertices or x == y:
            return False  # 非法输入

        for edge in self.adj_list[x]:
            if edge[0] == y:
                self.adj_list[x].remove(edge)
                self.num_edges -= 1
                return True
        return False

    def visualize(self, canvas):
        """图形化"""
        # 清空canvas
        canvas.delete('all')
        for widget in canvas.winfo_children():
            widget.destroy()

        # 计算每个节点的位置
        positions = self._compute_node_positions(canvas)

        # 画节点
        node_radius = 20
        for i, (x, y) in enumerate(positions):
            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
            canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))

        for i, (x, y) in enumerate(positions):
            canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='lightblue', outline='black')
            canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))

        # 画边
        self._draw_edges(canvas, positions)

    def draw_adjacency_list(self, canvas):
        """可视化邻接链表"""

        # 清空canvas
        canvas.delete('all')
        for widget in canvas.winfo_children():
            widget.destroy()

        # 位置参数
        start_x = 50  # 开始节点的x坐标
        start_y = 50  # 开始节点的y坐标
        gap_y = 80  # 垂直间隔
        gap_x = 100  # 水平间隔
        node_radius = 20  # 圆形节点半径
        rect_width = 40  # 正方形节点宽

        # 画邻接链表
        for i in range(self.num_vertices):
            # 画源点
            node_x1 = start_x - rect_width // 2
            node_y1 = start_y + i * gap_y - node_radius
            node_x2 = start_x + rect_width // 2
            node_y2 = start_y + i * gap_y + node_radius

            canvas.create_rectangle(node_x1, node_y1, node_x2, node_y2, fill="lightblue")
            canvas.create_text((node_x1 + node_x2) / 2, (node_y1 + node_y2) / 2, text=str(i),
                               font=("Arial", 12, "bold"))

            # 画邻接点
            for j, (adj_node, weight) in enumerate(self.adj_list[i]):
                # 圆心
                target_x = start_x + gap_x + j * gap_x
                target_y = start_y + i * gap_y
                # 画圆
                canvas.create_oval(target_x - node_radius, target_y - node_radius,
                                   target_x + node_radius, target_y + node_radius, fill="lightgreen")
                canvas.create_text(target_x, target_y, text=str(adj_node), font=("Arial", 12, "bold"))

                # 画箭头
                begin_x = target_x - gap_x + node_radius
                begin_y = target_y
                end_x = target_x - node_radius
                end_y = target_y
                canvas.create_line(begin_x, begin_y, end_x, end_y, arrow=tk.LAST)

                # 标权值
                weight_x = (target_x - gap_x + node_radius + target_x - node_radius) / 2
                weight_y = target_y - 12
                canvas.create_text(weight_x, weight_y, text=str(weight), fill="red", font=("Arial", 10))

    def topo_sort(self, canvas):
        """展示拓扑排序过程"""

        # 清空canvas
        canvas.delete('all')
        for widget in canvas.winfo_children():
            widget.destroy()

        # 初始化入度
        in_degree = [0] * self.num_vertices
        for vertices in self.adj_list:
            for vertex, _ in vertices:
                in_degree[vertex] += 1

        # 初始化零度队列
        zero_in_degree_queue = Queue()
        for v in range(self.num_vertices):
            if in_degree[v] == 0:
                zero_in_degree_queue.enqueue(v)

        topo_order = []  # 存储topo序列
        positions = self._compute_node_positions(canvas)  # 计算每个节点的位置
        step = 0

        # 开始拓扑排序动画
        while not zero_in_degree_queue.is_empty():
            # 绘制当前状态
            self._draw_graph(canvas, positions, in_degree, topo_order)
            canvas.update()
            time.sleep(0.5)  # 动画暂停

            # 处理队列中的下一个入度为0的节点
            vertex = zero_in_degree_queue.dequeue()
            topo_order.append(vertex)
            step += 1

            # 更新其邻居节点的入度
            for neighbor, _ in self.adj_list[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_in_degree_queue.enqueue(neighbor)

            # 更新画布
            self._draw_graph(canvas, positions, in_degree, topo_order)
            canvas.update()
            time.sleep(0.5)  # 动画暂停

        # 检查是否为有效的拓扑排序
        if len(topo_order) == self.num_vertices:
            return f"拓扑排序: {' >> '.join(map(str, topo_order))}"
        else:
            tk.messagebox.showerror("错误", "给定图包含回路")
            return '拓扑排序失败，非无环图'

    def critical_path(self, canvas):
        """求解并逐步显示关键路径"""

        # 清空canvas
        canvas.delete('all')
        for widget in canvas.winfo_children():
            widget.destroy()

        Width = canvas.winfo_width()
        Height = canvas.winfo_height()

        # 求topo序列
        # 1.初始化入度
        in_degree = [0] * self.num_vertices
        for vertices in self.adj_list:
            for vertex, _ in vertices:
                in_degree[vertex] += 1

        # 2.初始化零度队列
        zero_in_degree_queue = Queue()
        for v in range(self.num_vertices):
            if in_degree[v] == 0:
                zero_in_degree_queue.enqueue(v)

        topo_order = []  # 存储topo序列

        # 3.开始拓扑排序
        while not zero_in_degree_queue.is_empty():
            # 处理队列中的下一个入度为0的节点
            vertex = zero_in_degree_queue.dequeue()
            topo_order.append(vertex)

            # 更新其邻居节点的入度
            for neighbor, _ in self.adj_list[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_in_degree_queue.enqueue(neighbor)

        # 检查是否为有效的拓扑排序
        if len(topo_order) != self.num_vertices:
            tk.messagebox.showerror("错误", "给定图包含回路")
            canvas.delete('all')
            return '拓扑排序失败，非无环图'

        # 创建画布
        imageCanvas = tk.Canvas(canvas, width=Width / 2, height=Height, bg='white')
        imageCanvas.grid(row=0, column=0)
        tableCanvas = tk.Canvas(canvas, width=Width / 2, height=Height)
        tableCanvas.grid(row=0, column=1)

        # 图像部分
        imageCanvas.update()
        self.visualize(imageCanvas)

        # 表格部分

        # 1绘制表格
        headers = ["事件", "Ve", "Vl", "活动", "E", "L", "L-E"]
        # 绘制表头
        for i, header in enumerate(headers):
            tk.Label(tableCanvas, text=header, width=6, height=1, font=("黑体", 12, "bold"), anchor='center') \
                .grid(row=0, column=i)
        # 事件
        for u in range(self.num_vertices):
            tk.Label(tableCanvas, text=u, width=6, height=1, font=("黑体", 12, "bold"), anchor='center') \
                .grid(row=u + 1, column=0)
        canvas.update()
        # 初始化Ve（最早发生时间）
        Ve = [0] * self.num_vertices

        # 前向推导：计算Ve并逐步更新
        for u in topo_order:
            for v, weight in self.adj_list[u]:

                if Ve[u] + weight > Ve[v]:
                    Ve[v] = Ve[u] + weight
            self._draw_results_table(tableCanvas, u + 1, 1, Ve[u])  # 更新画布，显示当前Ve值

        # 初始化Vl（最迟发生时间）
        max_time = max(Ve)
        Vl = [max_time] * self.num_vertices

        # 反向推导：计算Vl并逐步更新
        for u in reversed(topo_order):
            for v, weight in self.adj_list[u]:
                if Vl[v] - weight < Vl[u]:
                    Vl[u] = Vl[v] - weight
            self._draw_results_table(tableCanvas, u + 1, 2, Vl[u])  # 更新画布，显示当前Ve值

        # 计算E（活动的最早开始时间）、L（活动的最迟开始时间）和L-E
        # 活动
        i = 1
        for u in topo_order:
            for v, _ in self.adj_list[u]:
                tk.Label(tableCanvas, text=f'{u}>>{v}', width=6, height=1, font=("黑体", 12, "bold"), anchor='center') \
                    .grid(row=i, column=3)
                i += 1
        E = []
        L = []
        slack = []  # L-E时间差

        i = 1
        for u in topo_order:
            for v, weight in self.adj_list[u]:
                e = Ve[u]  # 活动(u,v)的最早开始时间
                l = Vl[v] - weight  # 活动(u,v)的最迟开始时间
                E.append(('u>>v', e))
                L.append(('u>>v', l))
                slack.append(('u>>v', l - e))
                # 更新画布，显示当前E, L和slack值
                self._draw_results_table(tableCanvas, i, 4, e)
                self._draw_results_table(tableCanvas, i, 5, l)
                self._draw_results_table(tableCanvas, i, 6, l - e)
                i += 1
                # 如果在关键路径上（L-E == 0），用红色箭头绘制边
                if l - e == 0:
                    self._draw_edge_red(imageCanvas, u, v)

        # 绘制关键路径
        critical_path = [(u, v) for u in range(self.num_vertices) for v, weight in self.adj_list[u] if
                         Ve[u] == Vl[u] and Ve[v] == Vl[v]]

        return f"关键路径: {','.join(map(str, critical_path))}"

    def _draw_graph(self, canvas, positions, in_degree, topo_order):
        """绘制当前的图状态，包括节点、边和入度信息。"""
        canvas.delete('all')
        self._draw_edges(canvas, positions)
        self._draw_nodes(canvas, positions, in_degree)
        self._draw_topo_order(canvas, topo_order)

    def _draw_nodes(self, canvas, positions, in_degree):
        """绘制节点和入度信息。"""
        for i, (x, y) in enumerate(positions):
            color = 'lightblue' if in_degree[i] > 0 else 'red'  # 入度为0的节点变色
            canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline='black')
            canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))
            canvas.create_text(x, y + 30, text=f"入度: {in_degree[i]}", font=("宋体", 10))

    def _draw_edges(self, canvas, positions):
        """绘制边。"""
        for u in range(self.num_vertices):
            for v, w in self.adj_list[u]:
                x1, y1 = positions[u]
                x2, y2 = positions[v]

                # 修正直线起始和终点坐标
                dx, dy = x2 - x1, y2 - y1
                distance = math.sqrt(dx ** 2 + dy ** 2)

                x1 += 20 * dx / distance
                y1 += 20 * dy / distance
                x2 -= 20 * dx / distance
                y2 -= 20 * dy / distance
                # 画边
                canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

                # 计算直线中点
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2

                # 标权值
                r = 10
                canvas.create_oval(mid_x - r, mid_y - r, mid_x + r, mid_y + r, fill='white', outline='white')
                canvas.create_text(mid_x, mid_y, text=str(w), fill="red", font=("Arial", 10, "bold"))

    def _draw_topo_order(self, canvas, topo_order):
        """绘制拓扑排序顺序。"""
        canvas.create_text(400, 20, text=f"拓扑排序: {'>>'.join(map(str, topo_order))}",
                           font=("微软雅黑", 12, "bold"))

    def _compute_node_positions(self, canvas):
        """计算每个节点在画布上的位置，简单环形布局。"""
        num_vertices = self.num_vertices
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        center_x, center_y = width // 2, height // 2
        radius = min(center_x, center_y) - 50

        positions = []
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions.append((x, y))
        return positions

    def _draw_results_table(self, canvas, row, col, value):
        """在画布上逐步绘制结果表格，显示Ve, Vl, E, L和L-E。"""
        tk.Label(canvas, text=value, width=6, height=1, font=("黑体", 12, "bold"), anchor='center') \
            .grid(row=row, column=col)
        time.sleep(0.5)
        canvas.update()

        # # 绘制每个事件的结果
        # for i in range(self.num_vertices):
        #     canvas.create_text(start_x, start_y + (i + 1) * cell_height, text=f"{i}", font=("Arial", 10))
        #     if i < len(Ve) and Ve[i] != []:
        #         canvas.create_text(start_x + cell_width, start_y + (i + 1) * cell_height, text=f"{Ve[i]}",
        #                            font=("Arial", 10))
        #     if i < len(Vl) and Vl[i] != []:
        #         canvas.create_text(start_x + 2 * cell_width, start_y + (i + 1) * cell_height, text=f"{Vl[i]}",
        #                            font=("Arial", 10))
        #
        # # 绘制活动结果
        # for j in range(len(E)):
        #     canvas.create_text(start_x + 3 * cell_width, start_y + (j + 1) * cell_height, text=f"{E[j]}",
        #                        font=("Arial", 10))
        #     canvas.create_text(start_x + 4 * cell_width, start_y + (j + 1) * cell_height, text=f"{L[j]}",
        #                        font=("Arial", 10))
        #     canvas.create_text(start_x + 5 * cell_width, start_y + (j + 1) * cell_height, text=f"{slack[j]}",
        #                        font=("Arial", 10))

    def _draw_edge_red(self, imageCanvas, u, v):
        positions = self._compute_node_positions(imageCanvas)
        x1, y1 = positions[u]
        x2, y2 = positions[v]

        # 修正直线起始和终点坐标
        dx, dy = x2 - x1, y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2)

        x1 += 20 * dx / distance
        y1 += 20 * dy / distance
        x2 -= 20 * dx / distance
        y2 -= 20 * dy / distance
        # 画边
        imageCanvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill='gold', width=2)

        # 计算直线中点
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        # # 标权值
        # r = 10
        # imageCanvas.create_oval(mid_x - r, mid_y - r, mid_x + r, mid_y + r, fill='white', outline='white')
        # imageCanvas.create_text(mid_x, mid_y, text=str(w), fill="red", font=("Arial", 10, "bold"))


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("dequeue from an empty queue")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
