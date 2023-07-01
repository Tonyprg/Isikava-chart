import tkinter
from tkinter import font
import numpy
import math
from PIL import Image
from PIL import ImageTk

# -------------------------   ActiveFiled    ------------------------

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

    def draw (self, canvas, width = 1, fill = "black") :
        a, b = self.get_transform_points()
        ax, ay = a
        bx, by = b
        canvas.create_line(ax, ay, bx, by,
                           width = width,
                           fill = fill)


class Circle (Figure) :

    # Круг определяется двумя точками
    # 1-я точка - центр
    # 2-я точка - любая точка на окружности
    def __init__ (self, points) :
        super().__init__(points)
        self.text = ""

        self.image = None
        self.rimage = None
        self.photo = None

    def radius (self) :
        points = self.get_transform_points()
        return Line(points).length()

    # def draw (self, canvas, width = 1, outline = "black", fill = "white") :
    #     a, b = self.get_transform_points()
    #     x, y = a
    #     r = math.sqrt(
    #         (a[0] - b[0]) * (a[0] - b[0]) +
    #         (a[1] - b[1]) * (a[1] - b[1]))
    #     canvas.create_oval(
    #         x - r, y - r,
    #         x + r, y + r,
    #         width = width,
    #         outline = outline,
    #         fill = fill)
    #     fnt = font.Font(size = math.ceil(r / 4))
    #     canvas.create_text((x, y), text = self.text, font = fnt)

    def draw_with_text (self, canvas, width = 1, outline = "black", fill = "white") :
        a, b = self.get_transform_points()
        x, y = a
        r = math.sqrt(
            (a[0] - b[0]) * (a[0] - b[0]) +
            (a[1] - b[1]) * (a[1] - b[1]))
        canvas.create_oval(
            x - r, y - r,
            x + r, y + r,
            width = width,
            outline = outline,
            fill = fill)
        fnt = font.Font(size = math.ceil(r / 4))
        canvas.create_text((x, y), text = self.text, font = fnt)

    def draw_with_image (self, canvas, width = 1, outline = "black", fill = "white") :
        # Вычисление данных
        a, b = self.get_transform_points()
        x, y = a
        r = math.sqrt(
            (a[0] - b[0]) * (a[0] - b[0]) +
            (a[1] - b[1]) * (a[1] - b[1]))
        fnt = font.Font(size = math.ceil(r / 4))

        # Нарисовать круг
        canvas.create_oval(
            x - r, y - r,
            x + r, y + r,
            width = width,
            outline = outline,
            fill = fill)

        # Если в self.image записан объект Image(), то вывести его
        try :
            d = min(math.ceil(2 * r) - width, 150)
            self.rimage = self.image.resize((d, d))
            self.photo = ImageTk.PhotoImage(self.rimage)
            canvas.create_image(x, y, image = self.photo)
        except :
            canvas.create_text((x, y), text = self.text, font = fnt)

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


class ActiveField :

    def __init__ (self, root, width, height, figures = [], dbclick_left = None,
                                                           dbclick_right = None,
                                                           background = "white") :

        self.root = root
        self.width = width
        self.height = height
        self.background = background

        self.canvas = tkinter.Canvas(
            root,
            bg = self.background)
        self.canvas.pack(fill=tkinter.BOTH,expand=True)
        self.canvas.bind("<ButtonPress-1>", self.button_press)
        self.canvas.bind("<MouseWheel>", self.mouse_wheel)

        if dbclick_left :
            self.canvas.bind("<Double-ButtonPress-1>", dbclick_left)

        if dbclick_right :
            self.canvas.bind("<Double-ButtonPress-3>", dbclick_right)

        self.figures = figures
        self.draw()

    def draw (self) :
        for i in self.figures :
            i.draw(self.canvas)

    def clear (self) :
        self.canvas.delete('all')

    def redraw (self) :
        self.clear()
        self.canvas.config(bg = self.background)
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


class NodeFigure :

    def __init__ (self, lefl_line, circle, right_line) :
        self.left_line = lefl_line
        self.circle = circle
        self.right_line = right_line

        a, b = right_line.get_transform_points()
        self.tail = Line((b, b))

        self.func_draw = FuncDraw(self)

    def copy (self) :
        result = NodeFigure(
            self.left_line.copy(),
            self.circle.copy(),
            self.right_line.copy())
        return result

    def draw (self, canvas) :
        self.func_draw.draw(canvas)

    def width (self) :
        return   self.left_line.length() \
               + 2 * self.circle.radius() \
               + self.right_line.length()

    def height (self) :
        return 2 * self.circle.radius()

    def points (self) :
        a, b = self.left_line.get_transform_points()
        c, d = self.right_line.get_transform_points()
        return (a, b, c, d)

    def remove_tail (self) :
        a, b = self.right_line.get_transform_points()
        self.tail = Line((b, b))

    def translate  (self, dx, dy) :
        self.left_line.translate(dx, dy)
        self.circle.translate(dx, dy)
        self.right_line.translate(dx, dy)
        self.tail.translate(dx, dy)

    def rotate (self, angle, x = 0, y = 0) :
        self.translate(-x, -y)
        self.left_line.rotate(angle)
        self.circle.rotate(angle)
        self.right_line.rotate(angle)
        self.tail.rotate(angle)
        self.translate(x, y)

    def scale (self, k, x = 0, y = 0) :
        self.translate(-x, -y)
        self.left_line.scale(k)
        self.circle.scale(k)
        self.right_line.scale(k)
        self.tail.scale(k)
        self.translate(x, y)


class FuncDraw :

    def __init__ (self, node_figure, depth = 3) :
        self.node_figure = node_figure
        self.mark = False
        self.type = "node"

        self.left_line_width = (3 - depth) * 2
        self.left_line_fill = "black"

        self.circle_width = (3 - depth) * 2
        self.ciecle_outline = "black"
        self.circle_fill = "white"

        self.right_line_width = (3 - depth) * 2
        self.right_line_fill = "black"

        self.tail_depth = 0
        self.tail_width = (3 - depth) * 2
        self.tail_fill = "black"
        self.tail_ksep = None


    def set_depth (self, depth) :
        d = math.ceil(max((8 / (2 ** depth)), 1))
        self.left_line_width  = d
        self.circle_width     = d
        self.right_line_width = d
        self.tail_width       = d


    def set_width (self, width) :
        self.left_line_width  = width
        self.circle_width     = width
        self.right_line_width = width
        self.tail_width       = width


    def set_outline (self, color, child_color) :
        self.left_line_fill = color
        self.ciecle_outline = color
        self.right_line_fill = color
        self.tail_fill = (color, child_color)

        
    def draw (self, canvas) :

        self.node_figure.circle.draw_with_image(canvas,
            width   = self.circle_width,
            outline = self.ciecle_outline,
            fill    = self.circle_fill)

        if (self.type == "node") :
            self.node_figure.left_line.draw(canvas,
                width = self.left_line_width,
                fill  = self.left_line_fill)

            a, b = self.node_figure.tail.get_transform_points()
            (ax, ay), (bx, by) = a, b
            k = self.tail_ksep if self.tail_ksep else 0
            s = ax + (bx - ax) * k, \
                ay + (by - ay) * k
            Line((a, s)).draw(canvas,
                width = self.tail_width,
                fill  = self.tail_fill[0])
            Line((s, b)).draw(canvas,
                width = math.ceil(max((8 / (2 ** self.tail_depth)), 1)),
                fill  = self.tail_fill[1])

        elif (self.type == "root") :
            a, b = self.node_figure.tail.get_transform_points()
            (ax, ay), (bx, by) = a, b
            k = self.tail_ksep if self.tail_ksep else 0
            s = ax + (bx - ax) * k, \
                ay + (by - ay) * k
            Line((a, s)).draw(canvas,
                width = self.tail_width,
                fill  = self.tail_fill[0])
            Line((s, b)).draw(canvas,
                width = math.ceil(max((8 / (2 ** self.tail_depth)), 1)),
                fill  = self.tail_fill[1])

        elif (self.type == "leaf") :
            self.node_figure.left_line.draw(canvas,
                width = self.left_line_width,
                fill  = self.left_line_fill)
