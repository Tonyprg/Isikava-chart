import tkinter
import numpy
import math
import chart

class ShowChart :

    def __init__ (self, root, tree) :
        # общие данные
        self.width = 700
        self.height = 500
        self.tree = tree

        # Числовые данные фигур
        self.matrix = numpy.array([1, 0, 0, 0, 1, 0, 0, 0, 1], float).reshape(3, 3)
        self.figure = []

        # данные для теста
        self.create_leaf((self.width / 2, self.height / 2),
                         (self.width / 2 + 100, self.height / 2))
        self.create_leaf((self.width / 3, self.height / 3),
                         (self.width / 3 + 50, self.height / 3))

        # Данные tkinter
        self.root = root
        self.canvas = tkinter.Canvas(
            self.root,
            bg = "white",
            width = self.width,
            height = self.height)
        self.canvas.bind("<ButtonPress-1>", self.event_button_press)
        self.canvas.bind("<MouseWheel>", self.event_mouswheel)
        self.canvas.pack()

        self.draw()

    # Функции, осуществляющие рисование данных

    def transform (self, points) :
        """ функция умножает все точки в points на матрицу преобразования
        и возвращает новый кортеж, в котором записаны измененные точки """
        result = []
        for i in points :
            x, y = i
            v = self.matrix.dot(numpy.array([[x],[y], [1]], float)).reshape(3)
            result.append((v[0] / v[2], v[1] / v[2]))
        return tuple(result)

    def draw (self) :
        """ рисует все фигуры, которые добавлены в список
        self.figure, с учетом матрицы преобразования """
        for i in self.figure :
            i[0](self.transform(i[1]))

    def clear (self) :
        self.canvas.delete('all')

    def redraw (self) :
        self.clear()
        self.draw()

    def matrix_throw (self) :
        self.matrix = numpy.array([1, 0, 0, 0, 1, 0, 0, 0, 1], float).reshape(3, 3)

    # Функции, реагирующие на события мишы

    def event_button_press (self, event) :

        x, y = event.x, event.y    # начальная позиция
        dx, dy = 0, 0              # сдвиг

        def motion (event) :
            nonlocal x, y, dx, dy
            self.translate(-dx, -dy)
            dx, dy = event.x - x, event.y - y
            self.translate(dx, dy)

        def release (event) :
            self.canvas.unbind("<Motion>")

        self.canvas.bind("<Motion>", motion)
        self.canvas.bind("<ButtonRelease-1>", release)

    def event_mouswheel (self, event) :
        if event.delta > 0 : k = 1.1
        else : k = 0.9
        self.translate(-event.x, -event.y)
        self.scale(k)
        self.translate(event.x, event.y)

    # передвинуть весь рисунок на некоторый вектор
    def translate (self, dx, dy) :
        m = numpy.array([1, 0, dx, 0, 1, dy, 0, 0, 1], float).reshape(3, 3)
        self.matrix = m.dot(self.matrix)
        self.redraw()

    # увеличить/уменьшить рисунок
    def scale (self, k) :
        m = numpy.array([k, 0, 0, 0, k, 0, 0, 0, 1], float).reshape(3, 3)
        self.matrix = m.dot(self.matrix)
        self.redraw()

    # root_leaf
    def create_root_leaf (self, a, b) :
        self.figure.append([self.draw_root_leaf, (a, b)])

    def draw_root_leaf (self, args) :
        a, b = args
        x, y = a[0], a[1]
        r = math.sqrt(
            (a[0] - b[0]) * (a[0] - b[0]) +
            (a[1] - b[1]) * (a[1] - b[1]))

        self.canvas.create_oval(
            x - r, y - r,
            x + r, y + r)

    # root
    def create_root (self, a, b) :
        self.figure.append([self.draw_root, (a, b)])

    def draw_root (self, args) :
        a, b = args
        x, y = a[0], a[1]
        r = math.sqrt(
            (a[0] - b[0]) * (a[0] - b[0]) +
            (a[1] - b[1]) * (a[1] - b[1]))

        self.canvas.create_oval(
            x - r, y - r,
            x + r, y + r)
        self.canvas.create_line(
            x + r, y,
            x + 2 * r, y)

    # node
    def create_node (self, a, b) :
        self.figure.append([self.draw_node, (a, b)])

    def draw_node (self, args) :
        a, b = args
        x, y = a[0], a[1]
        r = math.sqrt(
            (a[0] - b[0]) * (a[0] - b[0]) +
            (a[1] - b[1]) * (a[1] - b[1]))

        self.canvas.create_oval(
            x - r, y - r,
            x + r, y + r)
        self.canvas.create_line(
            x - r - r * math.sqrt(2), y,
            x - r, y)
        self.canvas.create_line(
            x + r, y,
            x + 2 * r, y)

    #leaf
    def create_leaf (self, a, b) :
        self.figure.append([self.draw_leaf, (a, b)])

    def draw_leaf (self, args) :
        a, b = args
        x, y = a[0], a[1]
        r = math.sqrt(
            (a[0] - b[0]) * (a[0] - b[0]) +
            (a[1] - b[1]) * (a[1] - b[1]))

        self.canvas.create_oval(
            x - r, y - r,
            x + r, y + r)
        self.canvas.create_line(
            x - r - r * math.sqrt(2), y,
            x - r, y)

if __name__ == "__main__" :

    root = tkinter.Tk()
    sc = ShowChart(root, None)
    root.mainloop()

    # Это пока мусор
    tree =  chart.Tree()

    tree.insert("node1")
    tree.insert("node2", [], 0)
    tree.insert("node3", [], 1)
    tree.insert("node4", [], 2)
    tree.insert("node5", [], 3)

    tree.insert("node6", [1], 0)
    tree.insert("node7", [1], 1)
    tree.insert("node8", [1], 2)
    print(tree)
