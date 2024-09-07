import tkinter as tk
from tkinter import messagebox
from digraph import Digraph


class Application(tk.Frame):
    """GUI程序类"""

    def __init__(self, master=None):
        # 调用父类，初始化
        super().__init__(master, width=master.winfo_width(), height=master.winfo_width(), bg='white')
        self.pack()
        self.pack_propagate(False)  # 设置为False可使frame大小不变

        # 初始化图
        self.graph = Digraph(5)
        self.graph.add_edge(0, 2, 2)
        self.graph.add_edge(2, 4, 4)
        self.graph.add_edge(4, 1, 1)
        self.graph.add_edge(1, 3, 3)
        self.graph.add_edge(3, 0, 5)

        # 日志列表
        self.logs = []

        # 进入首页
        self.homePage()

    def homePage(self):
        """首页界面"""
        # 清空frame
        for widget in self.winfo_children():
            widget.destroy()

        # 更新窗口大小
        self.master.geometry('400x300')
        self.master.update()

        # 标签
        l = tk.Label(self, text='有向图可视化工具', bg='white', font=('华文行楷', 24, 'bold'), width=30, height=2)
        l.pack()
        # 开始
        start_btn = tk.Button(self, text='开始', font=('黑体', 12), bg='silver', width=15, height=2,
                              command=self.funcsPage)
        start_btn.pack()
        # 关于
        info_btn = tk.Button(self, text='关于', font=('黑体', 12), bg='silver', width=15, height=2,
                             command=self.authorPage)
        info_btn.pack()
        # 退出
        quit_btn = tk.Button(self, text='退出', font=('黑体', 12), bg='silver', width=15, height=2,
                             command=self.master.destroy)
        quit_btn.pack()

    def authorPage(self):
        """作者信息界面"""
        # 清空frame
        for widget in self.winfo_children():
            widget.destroy()

        # 更新窗口大小
        self.master.geometry('1200x750')
        self.master.update()

        # 设置背景颜色为水墨风格
        self.config(bg='white')

        # 显示作者信息
        title = tk.Label(self, text="作者信息", font=("KaiTi", 24, "bold"), fg="black", bg="white")
        title.pack(pady=20)

        info_frame = tk.Frame(self, bg='white')
        info_frame.pack(pady=30)

        # 作者信息文本
        info_texts = [
            "姓名: 李海禄",
            "学号: 2252933",
            "专业: 计算机科学与技术",
            "年级: 2022级",
            "课程信息: 同济大学 24年数据结构设计课程"
        ]

        # 文本标签
        for text in info_texts:
            label = tk.Label(info_frame, text=text, font=("KaiTi", 18), fg="black", bg="white")
            label.pack(anchor='w', pady=5)

        # 关闭按钮
        close_button = tk.Button(self, text='关闭', font=("KaiTi", 14), bg='black', fg='white', width=15, height=2,
                                 command=lambda: self.homePage())
        close_button.pack(pady=50)

        # 确保关闭按钮和信息始终在最上层
        close_button.lift()
        info_frame.lift()

    def funcsPage(self):
        """功能界面"""
        # 更新窗口大小
        self.master.geometry('1200x750')
        self.master.update()

        # 清空frame
        for widget in self.winfo_children():
            widget.destroy()

        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        # 导航栏
        navCanvas = tk.Canvas(self, width=canvas_width, height=canvas_height / 20, bg='cornflowerblue',
                              highlightthickness=0)
        navCanvas.pack()
        navCanvas.pack_propagate(False)
        # 按钮
        self.btns = {}
        for i in range(5):
            self.btns[i] = tk.Button(navCanvas, bg='cornflowerblue', fg='white', width=15, height=2, highlightthickness=0,
                                font=('黑体', 12), relief='flat')

        # 按钮属性赋值

        self.btns[0]['text'] = '显示图'
        self.btns[0]['command'] = lambda: self.graph.visualize(self.imageCanvas)

        self.btns[1]['text'] = '显示邻接表'
        self.btns[1]['command'] = lambda: self.graph.draw_adjacency_list(self.imageCanvas)

        self.btns[2]['text'] = '拓扑排序'
        self.btns[2]['command'] = lambda: [btnsDisabled(),
                                           self.log_operation(self.graph.topo_sort(self.imageCanvas)),
                                           btnsNormal()]  # 顺带更新日志

        self.btns[3]['text'] = '关键路径'
        self.btns[3]['command'] = lambda: [btnsDisabled(),
                                           self.log_operation(self.graph.critical_path(self.imageCanvas)),
                                           btnsNormal()]  # 顺带更新日志

        self.btns[4]['text'] = '返回'
        self.btns[4]['command'] = lambda: self.homePage()

        def btnsDisabled():
            # 按钮禁用
            for i in range(5):
                self.btns[i]['state'] = tk.DISABLED

        def btnsNormal():
            # 按钮禁用
            for i in range(5):
                self.btns[i]['state'] = tk.NORMAL

        # 按钮放置
        for i in range(5):
            self.btns[i].pack(side='left')

        # 内容画布
        contentCanvas = tk.Canvas(self, width=canvas_width, height=canvas_height * 19 / 20, bg='white',
                                  highlightthickness=0)
        contentCanvas.pack()

        inputCanvas = tk.Canvas(contentCanvas, width=canvas_width / 4, height=canvas_height - 4, bg='whitesmoke')
        inputCanvas.pack_propagate(False)  # 设置为False可使Canvas大小不变
        inputCanvas.pack(side='left')
        self.inputArea(inputCanvas)

        infoCanvas = tk.Canvas(contentCanvas, width=canvas_width * 3 / 4, height=canvas_height, highlightthickness=0)
        infoCanvas.pack(side='left')

        # 创建图像区域和文本区域
        self.imageCanvas = tk.Canvas(infoCanvas, width=canvas_width * 3 / 4, height=canvas_height * 2 / 3, bg='white',
                                highlightthickness=0)
        self.imageCanvas.pack()
        self.textCanvas = tk.Canvas(infoCanvas, width=canvas_width * 3 / 4, height=canvas_height / 3, bg='lightgrey')
        self.textCanvas.pack()

        self.master.update()  # 刷新
        self.imageArea()
        self.textArea()

    def inputArea(self, inputCanvas):
        canvas_width = inputCanvas.winfo_width()
        canvas_height = inputCanvas.winfo_height()

        # 修改节点部分
        # 1
        tk.Label(inputCanvas, text='修改节点数', bg="whitesmoke", fg='royalblue', font=('黑体', 14,), width=34,
                 height=1).pack()
        # 2
        modCanvas = tk.Canvas(inputCanvas, width=canvas_width, height=canvas_height / 3, bg='whitesmoke',
                              highlightthickness=0)
        modCanvas.pack()
        tk.Label(modCanvas, bg='whitesmoke', text='数量:').grid(row=0, column=0)
        entry_new_nodes = tk.Entry(modCanvas)
        entry_new_nodes.grid(row=0, column=1)
        b_modify_nodes = tk.Button(modCanvas, text='修改', command=lambda: self.modify_node_count(entry_new_nodes))
        b_modify_nodes.grid(row=1, column=1, pady=2, sticky='EW')

        # 插入边部分
        # 1
        tk.Label(inputCanvas, text='插入边', bg='whitesmoke', fg='royalblue', font=('黑体', 14,), width=30,
                 height=2).pack()
        # 2
        insCanvas = tk.Canvas(inputCanvas, width=canvas_width, height=canvas_height / 3, bg='whitesmoke',
                              highlightthickness=0)
        insCanvas.pack()
        tk.Label(insCanvas, bg='whitesmoke', text='源点:').grid(row=0, column=0)
        entry_from_node = tk.Entry(insCanvas)
        entry_from_node.grid(row=0, column=1)
        tk.Label(insCanvas, bg='whitesmoke', text='终点:').grid(row=1, column=0)
        entry_to_node = tk.Entry(insCanvas)
        entry_to_node.grid(row=1, column=1)
        tk.Label(insCanvas, bg='whitesmoke', text='权值:').grid(row=2, column=0)
        entry_weight = tk.Entry(insCanvas)
        entry_weight.grid(row=2, column=1)

        b_insert = tk.Button(insCanvas, text='插入',
                             command=lambda: self.insert_edge(entry_from_node, entry_to_node, entry_weight))
        b_insert.grid(row=3, column=1, sticky='WE')

        # 删除边部分
        # 1
        tk.Label(inputCanvas, text='删除边', bg='whitesmoke', fg='royalblue', font=('黑体', 14,), width=30,
                 height=2).pack()
        # 2
        delCanvas = tk.Canvas(inputCanvas, width=canvas_width, height=canvas_height / 3, bg='whitesmoke',
                              highlightthickness=0)
        delCanvas.pack()
        tk.Label(delCanvas, bg='whitesmoke', text='源点:').grid(row=0, column=0)
        entry_del_from_node = tk.Entry(delCanvas)
        entry_del_from_node.grid(row=0, column=1)
        tk.Label(delCanvas, bg='whitesmoke', text='终点:').grid(row=1, column=0)
        entry_del_to_node = tk.Entry(delCanvas)
        entry_del_to_node.grid(row=1, column=1)

        b_delete = tk.Button(delCanvas, text='删除',
                             command=lambda: self.delete_edge(entry_del_from_node, entry_del_to_node))
        b_delete.grid(row=2, column=1, sticky='WE')

        # 清除所有边
        b_clear = tk.Button(delCanvas, text='清除所有边', bg='red', fg='white', font=('黑体', 12),
                            command=self.clear_graph)
        b_clear.grid(row=3, column=1, sticky='WE')

        # 恢复默认
        b_init = tk.Button(delCanvas, text='恢复默认', bg='green', fg='white', font=('黑体', 12),
                           command=lambda: self.init())
        b_init.grid(row=4, column=1, sticky='WE')

    def imageArea(self):
        """输入界面"""
        # 清空canvas
        self.imageCanvas.delete('all')
        # 在imageCanvas上画图
        self.graph.visualize(self.imageCanvas)

    def textArea(self):
        # 清空canvas
        canvas_width = self.textCanvas.winfo_width()
        canvas_height = self.textCanvas.winfo_height()

        # 标头
        navCanvas = tk.Canvas(self.textCanvas, bg='royalblue', width=canvas_width, height=canvas_height/10)
        navCanvas .pack()
        navCanvas.create_text(10, 10, anchor='nw', text='操作日志', font=('黑体', 9))
        # 日志区域
        logCanvas = tk.Canvas(self.textCanvas, bg='lightgrey', width=canvas_width, height=canvas_height*9/10)
        self.log_text = tk.Text(logCanvas, bg='lightgrey', fg='black', font=('微软雅黑', 10), width=109)

        # 更新日志显示
        self.log_text.delete(0.0, tk.END)  # 清空日志框
        self.log_text.insert(tk.END, "\n".join(self.logs))  # 插入新的日志内容
        logCanvas.pack()
        self.log_text.pack(fill='both')

    def refreshText(self):
        self.log_text.delete(0.0, tk.END)  # 清空日志框
        self.log_text.insert(tk.END, "\n".join(self.logs))  # 插入新的日志内容

    def modify_node_count(self, entry_new_nodes):
        """修改节点数"""
        try:
            new_node_count = int(entry_new_nodes.get())
            if new_node_count <= 0:
                tk.messagebox.showerror("Error", "节点数量必须为正整数.")
                return

            if new_node_count < self.graph.num_vertices:
                # 节点数减少时删掉相关边
                self.graph.adj_list = self.graph.adj_list[:new_node_count]
                self.graph.num_vertices = new_node_count
                self.graph.num_edges = sum(len(adj) for adj in self.graph.adj_list)

                # 删掉指向被删除节点的边
                for adj in self.graph.adj_list:
                    adj[:] = [(v, w) for v, w in adj if v < new_node_count]

            elif new_node_count > self.graph.num_vertices:
                # 增加节点数
                self.graph.adj_list.extend([[] for _ in range(new_node_count - self.graph.num_vertices)])
                self.graph.num_vertices = new_node_count

            # tk.messagebox.showinfo("Success", "节点数已修改!")
            self.log_operation(f"节点数修改为 {new_node_count}")
            # 刷新
            self.refreshText()
            self.imageArea()

        except ValueError:
            tk.messagebox.showerror("Error", "非法输入，请输入正确整数.")

    def insert_edge(self, from_node_entry, to_node_entry, weight_entry):
        """在有向图中插入一条边"""
        try:
            from_node = int(from_node_entry.get())
            to_node = int(to_node_entry.get())
            weight = int(weight_entry.get())
            if self.graph.add_edge(from_node, to_node, weight):
                # tk.messagebox.showinfo("Success", "插入成功!")
                self.log_operation(f"添加边：{from_node} -> {to_node}, 权值 {weight}")
            else:
                tk.messagebox.showerror("Error", "插入失败，请确保输入节点在正确范围内.")
        except ValueError:
            tk.messagebox.showerror("Error", "非法输入，请输入正确整数.")
        # 刷新
        self.refreshText()
        self.imageArea()

    def delete_edge(self, from_node_entry, to_node_entry):
        """删除边."""
        try:
            from_node = int(from_node_entry.get())
            to_node = int(to_node_entry.get())
            if self.graph.remove_edge(from_node, to_node):
                # tk.messagebox.showinfo("Success", "边已删除!")
                self.log_operation(f"删除边：{from_node} -> {to_node}")
            else:
                tk.messagebox.showerror("Error", "边删除失败. 请检查边是否存在.")
        except ValueError:
            tk.messagebox.showerror("Error", "非法输入. 请输入正确整数.")
        # 刷新
        self.refreshText()
        self.imageArea()

    def clear_graph(self):
        """清空有向图"""
        self.graph = Digraph(self.graph.num_vertices)  # Reset graph to initial state with the same number of nodes
        # tk.messagebox.showinfo("Success", "所有边已清除!")
        self.log_operation("所有边已清除")
        # 刷新
        self.refreshText()
        self.imageArea()

    def init(self):
        self.graph = Digraph(5)
        self.graph.add_edge(0, 2, 2)
        self.graph.add_edge(2, 4, 4)
        self.graph.add_edge(4, 1, 1)
        self.graph.add_edge(1, 3, 3)
        self.graph.add_edge(3, 0, 5)
        self.log_operation("恢复默认")
        # 刷新
        self.refreshText()
        self.imageArea()

    def log_operation(self, message):
        """记录操作日志"""

        with open("operation_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")
        self.logs.append(message)
        self.refreshText()  # 刷新日志区
        print(message)  # 显示日志信息以调试


if __name__ == '__main__':
    window = tk.Tk()

    window.geometry('1200x750')
    window.title('有向图可视化工具')

    # 刷新
    window.update()
    # 应用
    app = Application(master=window)

    window.mainloop()
