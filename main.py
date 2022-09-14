import numpy as np
import random

ne2 = []
nex = []
ney = []
with open('NE.txt', 'r') as f:
    ne = f.readlines()
for i in range(len(ne)):#将txt写入，并删除\n，每行以空格分割两个字符串
    ne[i] = ne[i].rstrip('\n')
    ne2 += ne[i].split(None)

for i in range(len(ne2)):#将字符串转换成float
    ne2[i] = float(ne2[i])

for i in range(len(ne2)):#分开x和y值
    if i % 2 == 0:
        nex.append(ne2[i])
    elif i % 2 != 0:
        ney.append(ne2[i])

a = random.randint(1000000, 2000000)
b = random.randint(10000, 99999)
print(f"a = {a}, b = {b}")
nex2 = []
ney2 = []
for i in range(len(nex)):
    nex2.append(round(a * nex[i] + b, 6))
    ney2.append(round(a * ney[i] + b, 6))

ne_list = []
for i in range(len(nex2)):
    t = []
    t.append(nex2[i])
    t.append(ney2[i])
    ne_list.append(t)
print(ne_list)

class Node:
    def __init__(self, data, lchild = None, rchild = None):
        self.data = data
        self.lchild = lchild
        self.rchild = rchild

class KdTree:
    def __init__(self):
        self.kdTree = None

    def create(self, dataSet, depth):   #创建kd树，返回根结点
        if (len(dataSet) > 0):
            m, n = np.shape(dataSet)    #求出样本行，列
            midIndex = int(m / 2) #中间数的索引位置
            axis = depth % n    #判断以哪个轴划分数据
            sortedDataSet = self.sort(dataSet, axis) #进行排序
            node = Node(sortedDataSet[midIndex]) #将节点数据域设置为中位数
            #print sortedDataSet[midIndex]
            leftDataSet = sortedDataSet[: midIndex] #将中位数的左边创建2改副本
            rightDataSet = sortedDataSet[midIndex+1 :]
            #print(leftDataSet)
            #print(rightDataSet)
            node.lchild = self.create(leftDataSet, depth+1) #将中位数左边样本传入来递归创建树
            node.rchild = self.create(rightDataSet, depth+1)
            return node
        else:
            return None

    def sort(self, dataSet, axis):  #采用冒泡排序，利用aixs作为轴进行划分
        sortDataSet = dataSet[:]    #由于不能破坏原样本，此处建立一个副本
        m, n = np.shape(sortDataSet)
        for i in range(m):
            for j in range(0, m - i - 1):
                if (sortDataSet[j][axis] > sortDataSet[j+1][axis]):
                    temp = sortDataSet[j]
                    sortDataSet[j] = sortDataSet[j+1]
                    sortDataSet[j+1] = temp
        #print(sortDataSet)
        return sortDataSet

    def find(self, tree, x_low, x_high, y_low, y_high):
        xmin = x_low
        xmax = x_high
        ymin = y_low
        ymax = y_high

        def travel(node, depth):
            x = node.data[0]
            y = node.data[1]
            if xmin <= x and x <= xmax and ymin <= y and y <= ymax:
                print(node.data)
                FilePath = "text.txt"
                with open(FilePath, "a") as filewrite:  # ”a"代表着每次运行都追加txt的内容
                    filewrite.write(f"{node.data}\n")
            if depth % 2 == 0:#按x值
                if node.lchild != None:  # 左子树非空
                    if x > xmin:
                        travel(node.lchild, depth + 1)
                if node.rchild != None:  # 右子树非空
                    if x < xmax:
                        travel(node.rchild, depth + 1)
            else:#按y值
                if node.lchild != None:  # 左子树非空
                    if y > ymin:
                        travel(node.lchild, depth + 1)
                if node.rchild != None:  # 右子树非空
                    if y < ymax:
                        travel(node.rchild, depth + 1)

        travel(tree, 0)


dataSet = ne_list.copy()
kdtree = KdTree()
tree = kdtree.create(dataSet, 0)
#print(f"tree = {tree.data}")
a = input("输入范围下限，例如[1, 3]：")
b = input("输入范围上限，例如[1, 3]：")
a_list = list(eval(a))
b_list = list(eval(b))
print(f"范围下限为{a_list}，范围上限为{b_list}")
x_low = a_list[0]
y_low = a_list[1]
x_high = b_list[0]
y_high = b_list[1]
kdtree.find(tree, x_low, x_high, y_low, y_high)