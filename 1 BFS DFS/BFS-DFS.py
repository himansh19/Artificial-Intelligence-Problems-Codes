import math
class Node:
    def __init__(self, val: int):
        self.left = None
        self.right = None
        self.val = val

    def __repr__(self):
        return str(self.val)

    def insert_node(self, val):
        if self.val is not None:
            if val < self.val:
                if self.left is None:
                    self.left = Node(val)
                else:
                    self.left.insert_node(val)
            elif val > self.val:
                if self.right is None:
                    self.right = Node(val)
                else:
                    self.right.insert_node(val)

    @staticmethod
    def insert_nodes(vals: list, root):
        for i in vals:
            root.insert_node(i)

    def bfs(self, root=None):
        if root is None:    return
        queue = [root]
        lst=[]

        while len(queue) > 0:
            cur_node = queue.pop(0)
            lst.append(cur_node)
            # print(cur_node)
            if cur_node.left is not None:
                queue.append(cur_node.left)
            if cur_node.right is not None:
                queue.append(cur_node.right)

            print(queue,end=', ')
        print('\n')
        for x in lst: 
            print(x,end='-> ')
        print('\n')
    
    def dfs(self, root=None):
        if root is None:    return
        queue = [root]
        lst=[]
        
        while len(queue) > 0:
            cur_node = queue.pop()
            lst.append(cur_node)
            # print(cur_node)
            if cur_node.right is not None:
                queue.append(cur_node.right)
            if cur_node.left is not None:
                queue.append(cur_node.left)

            print(queue,end=', ')
        print('\n')
        for x in lst: 
            print(x,end='-> ')
        print('\n')


root = Node(4)
root.insert_nodes([2, 1, 3, 6, 5, 7], root)
hei=math.ceil(math.log2(6+1))
root.bfs(root)
root.dfs(root)

