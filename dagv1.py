import re


class TempVar(object):

    def __init__(self, name, cat="tempvar"):
        self.name = name
        self.cat = cat


class MiddleCode(object):

    def __init__(self, opt, item1=None, item2=None, res=None):
        self.opt = opt
        self.item1 = item1
        self.item2 = item2
        self.res = res

    def __str__(self):
        return "%s %s %s %s" % (self.opt, self.item1, self.item2, self.res)


class DAG_Node(object):

    def __init__(self, number, opt, *args):
        self.number = number  # 节点编码
        self.opt = opt  # 节点的运算符
        self.mark = list(args)  # 节点的标记, 首元素为主标记, 后面为附加标记
        self.leftNode = None
        self.rightNode = None


class DAG(object):

    def __init__(self):
        self.nodeList = list()
        self.exist = -1
        self.expr = -1

    def is_exist(self, item):
        for node in self.nodeList[::-1]:
            if item in node.mark:
                self.exist = node.number
                return True

    def is_expr_exist(self, opt, item1, item2):
        for node in self.nodeList:
            if (node.opt == opt and
                    item1 in self.nodeList[node.leftNode].mark and
                    item2 in self.nodeList[node.rightNode].mrak):
                self.expr = node.number
                return True

    def is_delete(self, item):
        for node in self.nodeList:
            if item in node.mark[1:]:
                node.mark.remove(item)


class Optimizer(object):  # 优化器

    def __init__(self):
        self.middle_codes = list()  # 中间代码-数据结构为列表
        self.dag = DAG()
        self.result = list()

    def load_middle_code(self, middle_codes):
        self.middle_codes = middle_codes

    def run(self):
        self.block_code()

    def block_code(self):
        low, high = 0, 0  # 代码块的下限与上限
        export_stat = ["if", "el", "wh", "do", "we", "ep","ie", "pro"]  # 出口语句
        nums = len(self.middle_codes)
        while high < nums:
            if self.middle_codes[high].opt in export_stat:
                if low <= high:
                    self.DAGborn(low, high)
                    self.DAGto_res()
                    self.dag.nodeList.clear()
                high += 1
                low = high
            else:
                high += 1


    def deal_int(self, number, a_int, res):
        if self.dag.is_exist(a_int):
            # 若这个常数在dag图中已经存在,则在这个节点的标记中添加上a
            self.dag.is_delete(res)
            self.dag.nodeList[self.dag.exist].mark.append(res)
        else:
            # 不存在, 则申请新节点, 注意标记信息
            new_node = DAG_Node(number, "=", a_int, res)
            self.dag.is_delete(res)
            self.dag.nodeList.append(new_node)

    def calculation(self, item1, item2, opt):
        temp = item1 + item2 if opt == "+" else 0
        temp = item1 - item2 if opt == "-" else temp
        temp = item1 * item2 if opt == "*" else temp
        temp = item1 / item2 if opt == "/" else temp
        temp = item1 > item2 if opt == ">" else temp
        temp = item1 < item2 if opt == "<" else temp
        temp = item1 == item2 if opt == "==" else temp
        temp = item1 >= item2 if opt == ">=" else temp
        temp = item1 <= item2 if opt == "<=" else temp
        return int(temp)

    def DAGborn(self, low, high):
        # print(low, high)  # for test
        opts = ["+", "-", "*", "/", ">", "<", "==", ">=", "<="]
        sp_opts = ["if", "el", "ie", "wh", "do", "we", "pro", "ret", "ep", "param", "call"]
        # 生成图信息
        while low <= high:
            mc = self.middle_codes[low]
            low += 1
            number = len(self.dag.nodeList)
            if mc.opt == "=":  # (= 1 _ a)
                if isinstance(mc.item1, int):
                    self.deal_int(number, mc.item1, mc.res)
                else:  # (= b _ a)
                    self.dag.is_exist(mc.item1)
                    self.dag.is_delete(mc.res)
                    self.dag.nodeList[self.dag.exist].mark.append(mc.res)
            elif mc.opt in opts:  # (+ 1 1 t1) (+ a b t1)
                if isinstance(mc.item1, int) and isinstance(mc.item2, int):  # 可以计算,就先计算
                    temp = self.calculation(mc.item1, mc.item2, mc.opt)
                    self.deal_int(number, temp, mc.res)
                else:  # 不可以计算
                    if self.dag.is_expr_exist(mc.opt, mc.item1, mc.item2):
                        # 已经存在此表达式
                        self.dag.is_delete(mc.res)
                        self.dag.nodeList[self.dag.expr].mark.append(mc.res)
                    else:
                        if self.dag.is_exist(mc.item1):
                            leftNode_number = self.dag.exist
                        else:
                            new_Node = DAG_Node(number, "=", mc.item1)
                            self.dag.nodeList.append(new_Node)
                            leftNode_number = number
                            number += 1
                        if self.dag.is_exist(mc.item2):
                            rightNode_number = self.dag.exist
                        else:
                            new_Node = DAG_Node(number, "=", mc.item2)
                            self.dag.nodeList.append(new_Node)
                            rightNode_number = number
                            number += 1
                        if (isinstance(self.dag.nodeList[leftNode_number].mark[0], int) and
                                isinstance(self.dag.nodeList[rightNode_number].mark[0], int)):
                            temp = self.calculation(self.dag.nodeList[leftNode_number].mark[0],
                                                    self.dag.nodeList[rightNode_number].mark[0],
                                                    mc.opt)
                            self.deal_int(number, temp, mc.res)
                        else:
                            new_Node = DAG_Node(number, mc.opt, mc.res)
                            new_Node.leftNode = leftNode_number
                            new_Node.rightNode = rightNode_number
                            self.dag.nodeList.append(new_Node)
            elif mc.opt in sp_opts:
                if mc.opt in ["pro"]:
                    new_Node = DAG_Node(number, mc.opt, mc.item1)
                    self.dag.nodeList.append(new_Node)
                if mc.opt in ["call"]:  # 把call当单目运算符处理
                    new_Node = DAG_Node(number, "=", mc.item1)
                    self.dag.nodeList.append(new_Node)
                    number += 1
                    new_Node = DAG_Node(number, mc.opt, mc.res)
                    new_Node.leftNode = number - 1
                    self.dag.nodeList.append(new_Node)
                if mc.opt in ["if", "do", "ret", "param"]:
                    if self.dag.is_exist(mc.item1):
                        leftNode_number = self.dag.exist
                    else:
                        new_Node = DAG_Node(number, "=", mc.item1)
                        self.dag.nodeList.append(new_Node)
                        leftNode_number = number
                        number += 1
                    new_Node = DAG_Node(number, mc.opt)
                    new_Node.leftNode = leftNode_number
                    self.dag.nodeList.append(new_Node)
                if mc.opt in ["el", "ei", "wh", "ew", "ep"]:
                    new_Node = DAG_Node(number, mc.opt)
                    self.dag.nodeList.append(new_Node)
        # 处理节点标记顺序
        for node in self.dag.nodeList:
            num = len(node.mark)
            if num <= 1:
                continue
            i = 0
            while i < num:
                if isinstance(node.mark[i], int):
                    temp = node.mark.pop(i) 
                    node.mark[1:] = node.mark[0:]
                    node.mark[0] = temp
                if not re.match(r't[0-9]+', str(node.mark[i])):  # 非临时变量
                    if not isinstance(node.mark[0], int):  # 且主标志不是常数
                        temp = node.mark.pop(i)
                        node.mark[1:] = node.mark[0:]
                        node.mark[0] = temp
                i += 1

    def DAGto_res(self):
        for node in self.dag.nodeList:
            if node.opt == "pro":
                mc = MiddleCode(node.opt, node.mark[0])
                self.result.append(mc)
            elif node.opt in ["if", "do", "ret", "param"]:
                mc = MiddleCode(node.opt, self.dag.nodeList[node.leftNode].mark[0], None, None)
                self.result.append(mc)
            elif node.opt in ["el", "ie", "wh", "we", "ep"]:
                mc = MiddleCode(node.opt)
                self.result.append(mc)
            elif node.opt == "call":
                mc = MiddleCode(node.opt, self.dag.nodeList[node.leftNode].mark[0], None, node.mark[0])
                self.result.append(mc)
            elif node.opt == "=":
                for m in node.mark[1:]:
                    if not re.match(r't[0-9]+', m):  # 非临时变量 [0-9]+
                        mc = MiddleCode(node.opt, node.mark[0], None, m)
                        self.result.append(mc)
            else:
                mc = MiddleCode(node.opt, self.dag.nodeList[node.leftNode].mark[0],
                                self.dag.nodeList[node.rightNode].mark[0], node.mark[0])
                self.result.append(mc)
                for m in node.mark[1:]:
                    if not re.match(r't[0-9]+', m):  # 非临时变量
                        mc = MiddleCode("=", node.mark[0], None, m)
                        self.result.append(mc)


# for test
def str_to_mid_code(mid_codes_str):
    mid_codes_lines = mid_codes_str.splitlines()
    mid_code_res = list()
    for mid_code_line in mid_codes_lines:
        if len(mid_code_line) == 0:
            break
        four_items = mid_code_line.split(" ")
        opt = four_items[0]
        if four_items[1].isdigit():  # 是数字类型
            item1 = int(four_items[1])
        elif four_items[1] == "_":  # 空
            item1 = None
        else:
            item1 = four_items[1]
        if four_items[2].isdigit():  # 是数字类型
            item2 = int(four_items[2])
        elif four_items[2] == "_":  # 空
            item2 = None
        else:
            item2 = four_items[2]
        if four_items[3] == "_":
            res = None
        else:
            res = four_items[3]
        mid_code_res.append(MiddleCode(opt, item1, item2, res))
    return mid_code_res


if __name__ == '__main__':
    with open("test.txt") as f:
        content = f.read()
    to_load = str_to_mid_code(content)
    for t in to_load:
        print(t)
    print("-" * 50)
    optimizer = Optimizer()
    optimizer.load_middle_code(to_load)
    optimizer.run()
    for ret in optimizer.result:
        print(ret)
