class VertexData () :

    def __init__ (self, image_path, text, date) :
        self.image_path = image_path
        self.text = text
        self.date = date
        pass

    def __str__ (self) :
        return "[image_path: {}, text: {}, date: {}]".\
            format(self.image_path, self.text, self.date)

class Tree () :

    def __init__ (self) :
        self.tree = []

    def __str__ (self) :
        if (self.tree == []) : return "[]"
        result = ""
        stack = [("", self.tree)]
        while (stack != []) :
            step, node = stack[-1]
            stack.pop()
            for i in range(len(node) - 1, 0, -1) :
                stack.append((step + "    ", node[i]))
            result += step + str(node[0]) + "\n"
        return result

    def get_node (self, path) :
        node = self.tree
        for i in path :
            node = node[i + 1]
        return node

    def insert (self, val, path = None, index = None) :
        if (self.tree == []) :
            self.tree = [val]
        else : self.get_node(path).insert(index + 1, [val])

    def swap (self, path, i, j) :
        node = self.get_node(path)
        node[i], node[j] = node[j], node[i]

    def romove (self, path, i) :
        self.get_node(path).pop(i)
