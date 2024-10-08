## 题目

给定一个有向图，完成： (1)建立并显示出它的邻接链表； (2)对该图进行拓扑排序，显示拓扑排序的结果，并随时显示入度域 的变化情况； (3)给出它的关键路径（要求：显示出 Ve，Vl，E，L，L-E 的结果）。

## 软件功能

### 1.图的建立与显示：

初始加载一个默认的有向图，用户可以使用图形化界面（GUI）进行动态修改。支持通过UI进行节点的插入、删除以及边的添加、删除操作，并在图形化界面中实时显示这些更改。

### 2.拓扑排序：

对有向图进行拓扑排序，动态显示排序过程，实时更新入度变化，最终显示排序结果。

### 3.关键路径计算：

通过拓扑排序结果计算出每个节点的 Ve（最早发生时间）、Vl（最迟发生时间），以及每条边的 E（活动最早开始时间）、L（活动最迟开始时间）和 L-E（松弛时间），并标识出关键路径。使用红色箭头动态显示关键路径。

### 4.图的显示与修改：

提供一个直观的图形化界面，允许用户实时查看和操作图的结构。用户可使用按钮进行插入、删除操作、修改节点数，以及恢复默认效果。

### 5.操作日志功能：

记录每次用户操作的日志（如插入节点、删除边等），并在日志区域显示，方便用户查看操作历史。

### 6.简洁美观的图形化界面：

使用Tkinter提供简洁明了的图形化界面设计，采用合适的颜色、布局和字体，使用户体验更加友好和直观。

## 开发平台

开发平台：Python 3.11，PyCharm作为IDE，运行环境为Windows 11。
依赖库：使用Python的Tkinter库实现图形化界面。以及time库实现延时效果，math库用于一些数学运算。
自定义模块：Graph和Queue类为自定义数据结构模块，负责图的操作与管理。

## 操作说明

1.启动程序后，进入首页界面。

![1](images/1.png)

2.点击开始进入功能页面。
功能界面有四个区域，顶部导航栏，左侧图输入区右侧图展示区以及底部的日志区域。

![2](images/2.png)

3.功能界面左侧实现对有向图的修改：
通过功能界面左侧的按钮进行插入节点、添加边、更改节点、删除边的操作，操作结果将在右侧画布中实时显示。

![5](images/5.png)

更改节点数目展示，有完备的错误处理功能

![3](images/3.png)![4](images/4.png)

修改成功后将实时在右侧区域展示修改后的图像，并在日志区留下操作记录。

插入和删除，指定源点和终点，给出对应权值可实现插入删除，也有完备的错误处理，不能插入已有边，不能删除不存在的边，以及不能处理一些非法边，都会弹出提示

![6](images/6.png)![7](images/7.png)

清除所有边和恢复默认功能按钮效果如其所说一致。
4.拓扑排序：
点击“开始拓扑排序”按钮，程序将自动执行拓扑排序并动态显示排序过程。

![8](images/8.png)

注意拓扑排序需要图是无环图，若不满足会弹出错误提示窗口。

![9](images/9.png)

拓扑排序期间禁用导航栏来规避不必要的系统错误。

5.关键路径计算：
拓扑排序完成后，点击“计算关键路径”按钮，程序逐步显示关键路径计算过程，并用金色箭头标记关键路径。

![10](images/10.png)

6.操作日志查看：
操作日志区域显示用户的每一步操作，如插入节点、删除边、拓扑排序、关键路径结果等。每次用户操作后，操作日志区域显示相应记录，便于用户查看操作历史。

![11](images/11.png)
