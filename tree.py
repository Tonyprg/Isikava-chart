import math
import tkinter
import random

import active_field as af

class NodeData :

    def __init__ (self, figure = None) : 
        self.figure = figure

        self.header = None
        self.text = None
        self.date = None
        self.priority = None

    def __str__ (self) :
        s = "header  : {},\n".format(self.header) + \
            "text    : {},\n".format(self.text) + \
            "date    : {},\n".format(self.date) + \
            "priority: {} \n".format(self.priority)
        return s

    def copy (self) :
        return NodeData(self.figure.copy())


class Node :


    def __init__ (self, data, parent = None, path = None, index = None) :

        self.data = data
        self.parent = parent
        self.path = path
        self.index = index
        self.child = []

    def __str__ (self) :
        result = ""
        stack = [("", self)]
        while stack != [] :
            step, node = stack.pop()
            result += step + str(node.data) + "\n"
            for i in range(len(node.child) - 1, -1, -1) :
                stack.append((step + "    ", node.child[i]))
        return result


    def __iter__ (self) :
        stack = [self]
        while stack != [] :
            node = stack.pop()
            yield node
            for i in range(len(node.child) - 1, -1, -1) :
                stack.append(node.child[i])


    def write_file (self, file_name) :
        file = open(file_name, "w")
        for i in self :
            node = {
                "header"   : i.data.header,
                "text"     : i.data.text,
                "date"     : i.data.date,
                "priority" : i.data.priority,
                "path"     : i.path,
                "index"    : i.index
            }
            file.write(str(node) + "\n")
        file.close()


    def read_file (self, file_name) :
        file = open(file_name, "r")
        for i in file :
            data = eval(i)
            node = Node(NodeData())
            node.data.header   = data["header"]
            node.data.text     = data["text"]
            node.data.date     = data["date"]
            node.data.priority = data["priority"]
            node.path = data["path"]
            node.index = data["index"]
            self.insert(node.data, node.path, node.index)

        file.close()



    def set_path (self, path = None, index = None) :
        if path == None :
            self.path = None
            self.index = None
            for (i, child) in enumerate(self.child) :
                child.set_path([], i)
        else :
            self.path = path.copy()
            self.index = index
            for (i, child) in enumerate(self.child) :
                child.set_path(path.copy() + [index], i)


    def insert (self, data, path, index) :
        node = self
        for i in path :
            node = node.child[i]
        node.child.insert(index, Node(data, node, path, index))


    def delete (self, path, index) :
        if path == None :
            return None
        node = self
        for i in path :
            node = node.child[i]
        node.child.pop(index)
        self.set_path()


    def create_figures (self, figure = af.NodeFigure(
                                           af.Line(((100, 250), (150, 250))),
                                           af.Circle(((200, 250), (250, 250))),
                                           af.Line(((250, 250), (300, 250)))),
                              colors = ["black"],
                              fill_color = "white") :

        stack = [(0, self)]
        while (stack != []) :
            depth, node = stack.pop()
            node.data.figure = figure.copy()
            # отобразить текст на узле
            if node.data.header :
                node.data.figure.circle.text = node.data.header

            # определение типа узла
            if node.parent == None and node.child == [] :
                node.data.figure.func_draw.type = "root_leaf"
            elif node.parent == None :
                node.data.figure.func_draw.type = "root"
            elif node.child == [] :
                node.data.figure.func_draw.type = "leaf"

            # Цвет узлов и ребер и ширина ребер
            node.data.figure.func_draw.set_depth(depth)
            node.data.figure.func_draw.circle_fill = fill_color
            node.data.figure.func_draw.set_outline(colors[min(depth, len(colors) - 1)])

            for i in node.child :
                stack.append((depth + 1, i))

        # установка начальных значений для корня
        self.edit_figures()


    def edit_figures (self, k = 0.5, angle = 60 * math.pi / 180) :

        # необходимые данные
        a, b = self.data.figure.left_line.get_transform_points()
        c, d = self.data.figure.right_line.get_transform_points()
        (ax, ay), (bx, by), (cx, cy), (dx, dy) = a, b, c, d

        width = af.Line((b, c)).length()
        height = width
        step = width / 2 / math.tan(angle) - af.Line((a, b)).length()
        if step < 0 :
            height -= step
            step = 0

        if self.child == [] :
            return step, width, height

        height += af.Line((c, d)).length()

        for index, child in enumerate(self.child) :

            # первоначальное изменение позиции и размеров
            for node in child :
                data = node.data

                if index % 2 == 0 :
                    data.figure.rotate(angle, ax, ay)
                else :
                    data.figure.rotate(-angle, ax, ay)

                data.figure.scale(k, ax, ay)

                ab = af.Line((a, b)).length()
                data.figure.translate(
                    (bx - ax) / ab * (height + width / 2 / math.tan(angle) - step),
                    (by - ay) / ab * (height + width / 2 / math.tan(angle) - step))

            s, w, h = child.edit_figures()

            if angle > 45 * math.pi / 180 :

                left_pr = h * math.cos(angle)
                right_pr = w * math.sin(angle)
                vertical_pr = h * math.sin(angle) + w * math.cos(angle)
                full_height = height + width / 2 / math.tan(angle)

                if w * math.cos(angle) < full_height * math.tan(angle) :

                    # корректировка позиции (второе изменение)
                    for node in child :
                        data = node.data
                        data.figure.translate(
                                (bx - ax) / ab * (-w / 2 / math.sin(angle) * math.cos(2 * angle)),
                                (by - ay) / ab * (-w / 2 / math.sin(angle) * math.cos(2 * angle)))

                    if vertical_pr > width / 2 :
                        height = left_pr + right_pr - (vertical_pr / math.tan(angle) - full_height)
                        width = 2 * vertical_pr
                    else :
                        height += left_pr + right_pr

                else :

                    # корректировка позиции (так же второе изменение, т.к. в ветке else)
                    for node in child :
                        data = node.data
                        data.figure.translate(
                                (bx - ax) / ab * (w / 2 / math.sin(angle) - full_height),
                                (by - ay) / ab * (w / 2 / math.sin(angle) - full_height))

                    height = left_pr + right_pr
                    width = vertical_pr

        # p = dx + (dx - cx) / af.Line((c, d)).length() * height, \
        #     dy + (dy - cy) / af.Line((c, d)).length() * height
        # self.data.figure.tail = af.Line((d, p))

        if self.child != [] :
            p, q = self.child[-1].data.figure.left_line.get_transform_points()
            px, py = p
            p = px + (dx - cx) / af.Line((c, d)).length() * af.Line((p, q)).length(), \
                py + (dy - cy) / af.Line((c, d)).length() * af.Line((p, q)).length()

            self.data.figure.tail = af.Line((d, p))

        return step, width, height


class Chart :


    def __init__ (self, root, name = "", width = 800, height = 500) :
        self.name = name

        self.node_outline = ["gray"]
        self.node_fill = "white"
        self.mark_fill = "blue"

        self.head = Node(NodeData())
        self.head.create_figures(
            colors = self.node_outline,
            fill_color = self.node_fill)

        self.mark = self.head
        self.mark.data.figure.func_draw.circle_fill = self.mark_fill

        self.field_background = "#FFE773"
        self.field = af.ActiveField(root, width, height,
                                    [i.data.figure for i in self.head],
                                    lambda event: self.double_click_left(event),
                                    lambda event: self.double_click_right(event),
                                    background = self.field_background)


    def double_click_left (self, event) :

        for i in self.head :

            (px, py), _ = i.data.figure.circle.get_transform_points()
            r = i.data.figure.circle.radius()

            if (event.x - px) ** 2 + (event.y - py) ** 2 < r * r:
                if self.mark == i :
                    break

                self.mark.data.figure.func_draw.circle_fill = self.node_fill

                self.mark = i
                self.mark.data.figure.func_draw.circle_fill = self.mark_fill

                break

        self.field.redraw()

    def double_click_right (self, event) :

        for i in self.head :

            (px, py), _ = i.data.figure.circle.get_transform_points()
            r = i.data.figure.circle.radius()

            if (event.x - px) ** 2 + (event.y - py) ** 2 < r * r:
                self.mark.data.header, i.data.header = i.data.header, self.mark.data.header 
                self.mark.data.figure.circle.text, i.data.figure.circle.text = \
                    i.data.figure.circle.text, self.mark.data.figure.circle.text
                self.mark.data.text, i.data.text = i.data.text, self.mark.data.text
                self.mark.data.date, i.data.date = i.data.date, self.mark.data.date
                self.mark.data.priority, i.data.priority = i.data.priority, self.mark.data.priority
                break

        self.field.redraw()

    def write_file (self, file_name) :
        file = open(file_name, "w")
        file.write(self.name + "\n")
        for i in self.head :
            node = {
                "header"   : i.data.header,
                "text"     : i.data.text,
                "date"     : i.data.date,
                "priority" : i.data.priority,
                "path"     : i.path,
                "index"    : i.index
            }
            file.write(str(node) + "\n")
        file.close()


    def read_file (self, file_name) :
        self.head = None
        file = open(file_name, "r")
        read_name = False
        for i in file :
            if not read_name :
                self.name = i[:-1]
                read_name = True
                continue
            data = eval(i)
            node = Node(NodeData())
            node.data.header   = data["header"]
            node.data.text     = data["text"]
            node.data.date     = data["date"]
            node.data.priority = data["priority"]
            node.path = data["path"]
            node.index = data["index"]
            if self.head == None :
                self.head = node
            else :
                self.head.insert(node.data, node.path, node.index)
        file.close()

        self.head.create_figures(
            colors = self.node_outline,
            fill_color = self.node_fill)

        self.mark = self.head
        self.mark.data.figure.func_draw.circle_fill = "blue"

        self.field.figures = [i.data.figure for i in self.head]
        self.field.redraw()


    def append_node (self) :
        """ Добавляет узел к ветке, на корень которой указывает self.mark"""

        if self.mark == self.head :
            self.mark.insert(NodeData(), [], len(self.mark.child))
        else :
            path = self.mark.path.copy()
            path.append(self.mark.index)
            self.head.insert(NodeData(), path, len(self.mark.child))

        self.head.data.figure.remove_tail()
        self.head.create_figures(
            self.head.data.figure,
            colors = self.node_outline,
            fill_color = self.node_fill)

        self.mark.data.figure.func_draw.circle_fill = self.mark_fill
        
        self.field.figures = [i.data.figure for i in self.head]
        self.field.redraw()


    def remove_node (self) :
        """ Удаляет узел, на который указывает self.mark """
        
        if self.mark == self.head :
            return None

        self.head.delete(self.mark.path, self.mark.index)

        self.head.data.figure.remove_tail()
        self.head.create_figures(
            self.head.data.figure,
            colors = self.node_outline,
            fill_color = self.node_fill)

        self.mark = self.head
        self.mark.data.figure.func_draw.circle_fill = self.mark_fill

        self.field.figures = [i.data.figure for i in self.head]
        self.field.redraw()


    def get_header (self) :
        return self.mark.data.header


    def get_text (self) :
        return self.mark.data.text


    def get_date (self) :
        return self.mark.data.date


    def get_priority (self) :
        return self.mark.data.priority


    def set_header (self, header) :
        self.mark.data.figure.circle.text = header
        self.mark.data.header = header


    def set_text (self, text) :
        self.mark.data.text = text


    def set_date (self, date) :
        self.mark.data.date = date


    def set_priority (self, priority) :
        self.mark.data.priority = priority


    def set_style (self, name_file) :
        f = open("style/" + name_file, "r");
        style = eval(f.read())
        f.close()

        self.node_outline = style["outline"].copy()
        self.node_fill = style["node_fill"]
        self.mark_fill = style["mark_fill"]
        self.field_background = style["background"]
        self.head.create_figures(
            self.head.data.figure,
            colors = self.node_outline,
            fill_color = self.node_fill)
        self.mark.data.figure.func_draw.circle_fill = self.mark_fill
        self.field.figures = [i.data.figure for i in self.head]
        self.field.background = self.field_background
        self.field.redraw()


if __name__ == "__main__" :

    root = tkinter.Tk()
    root.state("zoomed")
    crt = Chart(root)
    # crt.read_file("charts/Диаграмма")

    tkinter.Button(root, text = "append", command = crt.append_node).pack()
    tkinter.Button(root, text = "remove", command = crt.remove_node).pack()

    tkinter.Button(root, text = "write_file", command = lambda: crt.write_file("charts/Диаграмма")).pack()

    crt.set_style("default")

    root.mainloop()
