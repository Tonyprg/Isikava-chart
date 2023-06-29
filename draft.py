import tkinter
import numpy
import math
import chart
import tree

class Figure :

    def __init__ (self, points) :

        self.points = tuple(points) 

        self.matrix = numpy.array(
            [1,0,0,0,1,0,0,0,1],
            float).reshape(3, 3)

    def __str__ (self) :
        return str(self.points) + "\n" + str(self.matrix) + "\n"

    def copy (self) :
        result = type(self)(self.points)
        result.matrix = self.matrix.copy()
        return result

    def get_transform_points (self) :
        result = []
        for i in self.points :
            x, y = i
            v = numpy.array([x, y, 1], float).reshape(3, 1)
            v = self.matrix.dot(v).reshape(3)
            result.append((v[0], v[1]))
        return tuple(result)

    def rotate_matrix (self, angle) :
        return numpy.array(
            # матрица отличается от стандартной, т.к.
            # система координат на canvas имеет положительное
            # направление движения по часовой стрелке
            [math.cos(angle),  math.sin(angle), 0,
             -math.sin(angle), math.cos(angle), 0,
                           0,                0, 1],
            float).reshape(3, 3)

    def translate_matrix (self, dx, dy) :
        return numpy.array(
            [1, 0, dx,
             0, 1, dy,
             0, 0,  1],
            float).reshape(3, 3)

    def scale_matrix (self, k) :
        return numpy.array(
            [k, 0, 0,
             0, k, 0,
             0, 0, 1],
            float).reshape(3, 3)

    def rotate (self, angle) :
        self.matrix = self.rotate_matrix(angle).dot(self.matrix)

    def translate (self, dx, dy) :
        self.matrix = self.translate_matrix(dx, dy).dot(self.matrix)

    def scale (self, k) :
        self.matrix = self.scale_matrix(k).dot(self.matrix)

    def default (self) :
        self.matrix = numpy.array(
            [1,0,0,0,1,0,0,0,1],
            float).reshape(3, 3)


class Line (Figure) :

    def __init__ (self, points) :
        super().__init__(points)

    def length (self) :
        a, b = self.get_transform_points()
        ax, ay = a
        bx, by = b
        dx = bx - ax
        dy = by - ay
        return math.sqrt(dx * dx + dy * dy)

    def draw (self, canvas) :
        a, b = self.get_transform_points()
        ax, ay = a
        bx, by = b
        canvas.create_line(ax, ay, bx, by)


class Circle (Figure) :

    # Круг определяется двумя точками
    # 1-я точка - цент
    # 2-я точка - любая точка на окружности
    def __init__ (self, points) :
        super().__init__(points)

    def radius (self) :
        points = self.get_transform_points()
        return Line(points).length()

    def draw (self, canvas) :
        a, b = self.get_transform_points()
        x, y = a
        r = math.sqrt(
            (a[0] - b[0]) * (a[0] - b[0]) +
            (a[1] - b[1]) * (a[1] - b[1]))
        canvas.create_oval(
            x - r, y - r,
            x + r, y + r)


class Rectangle (Figure) :

    def __init__ (self, points) :
        super().__init__(points)

    def draw (self, cavnas) :
        a, b = self.get_transform_points()
        ax, ay = a
        bx, by = b
        canvas.create_rectangle(ax, ay, bx, by)


class Oval (Figure) :

    def __init__ (self, points) :
        super().__init__(points)

    def draw (self, canvas) :
        a, b = self.get_transform_points()
        ax, ay = a
        bx, by = b
        canvas.create_oval(ax, ay, bx, by)

class NodePicture :

    def __init__ (self, lefl_line, circle, right_line) :
        self.left_line = lefl_line
        self.circle = circle
        self.right_line = right_line

        self.draw = self.draw_node

    def copy (self) :
        return Node(
            self.lefl_line.copy(),
            self.circle.copy(),
            self.right_line.copy())

    def width (self) :
        return   self.left_line.length() \
               + 2 * self.circle.radius() \
               + self.right_line.length()

    def height (self) :
        return 2 * self.circle.radius()

    def draw_root_leaf (self, canvas) :
        self.circle.draw(canvas)

    def draw_root (self, canvas) :
        self.circle.draw(canvas)
        self.right_lien.draw(canvas)

    def draw_leaf (self, canvas) :
        self.left_line.draw(ccanvas)
        self.circle.draw(canvas)

    def draw_node (self, canvas) :
        self.left_line.draw(canvas)
        self.circle.draw(canvas)
        self.right_line.draw(canvas)

    def translate  (self, dx, dy) :
        self.left_line.translate(dx, dy)
        self.circle.translate(dx, dy)
        self.right_line.translate(dx, dy)

    def rotate (self, angle) :
        a, _ = self.left_line.get_transform_points()
        x, y = a
        self.translate(-x, -y)
        self.left_line.rotate(angle)
        self.circle.rotate(angle)
        self.right_line.rotate(angle)
        self.translate(x, y)

    def scale (self, k) :
        a, _ = self.left_line.get_transform_points()
        x, y = a
        self.translate(-x, -y)
        self.left_line.scale(k)
        self.circle.scale(k)
        self.right_line.scale(k)
        self.translate(x, y)

class ActiveField :

    def __init__ (self, root, width, height, figures) :

        self.root = root
        self.width = width
        self.height = height

        self.canvas = tkinter.Canvas(
            root,
            bg = "white",
            width = self.width,
            height = self.height)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.button_press)
        self.canvas.bind("<MouseWheel>", self.mouse_wheel)

        self.figures = figures
        self.draw()

    def draw (self) :
        for i in self.figures :
            i.draw(self.canvas)

    def clear (self) :
        self.canvas.delete('all')

    def redraw (self) :
        self.clear()
        self.draw()

    def rotate (self, angle) :
        for i in self.figures :
            i.rotate(angle)

    def translate (self, dx, dy) :
        for i in self.figures :
            i.translate(dx, dy)

    def scale (self, k) :
        for i in self.figures :
            i.scale(k)

    def button_press (self, event) :

        def motion (event) :
            nonlocal x, y, dx, dy
            self.translate(-dx, -dy)
            dx = event.x - x
            dy = event.y - y
            self.translate(dx, dy)
            self.redraw()

        def release (event) :
            nonlocal x, y, dx, dy
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

        x, y = event.x, event.y
        dx, dy = 0, 0
        self.canvas.bind("<Motion>", motion)
        self.canvas.bind("<ButtonRelease-1>", release)
        self.redraw()

    def mouse_wheel (self, event) :
        k = 1.1
        if (event.delta < 0) :
            k = 0.9
        self.translate(-event.x, -event.y)
        self.scale(k)
        self.translate(event.x, event.y)
        self.redraw()

# def figures_of_tree (tree) :

#     queue = [tree]
#     while (queue != []) :

#         node = queue[0]
#         print(node[0])

#         queue.pop(0)
#         for i in range(1, len(node)) :
#             queue.append(node[i])
#     return [Line(((0, 0), (100, 100)))]

def figures_of_tree (tree,
                     k = 0.5,
                     line = Line(((100, 250), (200, 250)))) :

    result = []
    width = line.length()
    height = 0

    for i in range(len(tree.child)) :

        a, b = line.get_transform_points()
        ax, ay = a
        bx, by = b
        dx = (bx - ax) * (i + 1)
        dy = (by - ay) * (i + 1)

        # translate
        line.translate(dx, dy)
        result.append(line.copy())
        # reverse translate
        line.translate(-dx, -dy)

        # rotate and scale
        line.translate(-ax, -ay)
        line.rotate(((-1) ** i) * 45 * math.pi / 180)
        line.scale(k)
        line.translate(ax, ay)

        # translate
        line.translate(dx, dy)

        fgs, w, h = figures_of_tree(tree.child[i], k, line)
        result += fgs.copy()

        # reverse translate
        line.translate(-dx, -dy)

        # reverse rotate and reverse scale
        line.translate(-ax, -ay)
        line.rotate(((-1) ** (i + 1)) * 45 * math.pi / 180)
        line.scale(1 / k)
        line.translate(ax, ay)

    result += [line.copy()]

    return (result, width, height)

tr = tree.Node(0)
tr.insert(1, [], 0)
tr.insert(2, [], 1)
tr.insert(3, [], 2)
tr.insert(4, [], 3)
tr.insert(5, [1], 0)
tr.insert(6, [1], 1)
tr.insert(7, [2], 0)
tr.insert(8, [2], 1)
tr.insert(9,  [1, 0], 0)
tr.insert(10, [1, 0], 1)
tr.insert(11, [1, 0], 2)
tr.insert(12, [2, 0], 0)
tr.insert(13, [2, 0], 1)
tr.insert(14, [1, 0, 2], 0)
tr.insert(15, [1, 0, 2], 1)

root = tkinter.Tk()

af = ActiveField(root, 800, 500, figures_of_tree(tr)[0])

root.mainloop()
