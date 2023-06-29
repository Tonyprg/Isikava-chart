from tkinter import *
import tkinter
from tkinter import ttk
import stack_menu
import charts_view_and_edit_page_window as sf
from PIL import Image
import tree
import datetime
from PIL import Image, ImageTk


class ChartsViewPageWindow:
    def __init__(self, master, smw, chart_name, style, language):
        self.master = master
        self.smw = smw
        self.chart_name = chart_name
        self.style = style
        self.language = language

        self.smw.get().configure(style="BG.TFrame")

        self.left_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")
        self.left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.chart = tree.Chart(self.left_frame, chart_name)
        self.chart.read_file('charts\\' + self.chart_name)

        self.chart.field.canvas.bind("<Double-ButtonPress-1>", self.update_view)

        self.back_button = ttk.Button(self.left_frame, text=self.language.get_text('back'), command=self.back, style="Btn.TButton")
        self.back_button.pack(side=tkinter.BOTTOM, anchor="sw", padx=10, pady=10)

        self.right_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")
        self.right_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=False)

        self.local_stack = stack_menu.StackMenuWidget(self.right_frame)
        self.local_stack.get().configure(style="SubMenu.TFrame")

        self.header_view_head = ttk.Label(self.local_stack.get(),
                                          text=self.language.get_text('header'),
                                          style="Header.TLabel")
        self.header_view_head.pack(fill=tkinter.X)

        self.header_view = ttk.Label(self.local_stack.get(),
                                     text=self.chart.get_header() if self.chart.get_header() else "-пусто-",
                                     style="Text.TLabel")
        self.header_view.pack(padx=10, pady=10, fill=tkinter.X)

        self.node_text_label_head = ttk.Label(self.local_stack.get(),
                                              text=self.language.get_text('content'),
                                              style="Header.TLabel")  # text (откуда брать текст)
        self.node_text_label_head.pack(fill=tkinter.X)

        self.node_text_label = ttk.Label(self.local_stack.get(),
                                         text=self.chart.get_text() if self.chart.get_text() else "-пусто-",
                                         style="Text.TLabel")  # text (откуда брать текст)
        self.node_text_label.pack(padx=10, pady=10, fill=tkinter.X)

        # self.edited_image = PhotoImage(file="photoes/edited.png").subsample(3)  # cropped image (откуда брать и куда оно должно сохраняться)
        #
        # self.view = ttk.Label(self.local_stack.get(),
        #                       image=self.edited_image,
        #                       style="Image.TLabel")
        # self.view.pack(padx=10, pady=10, fill=tkinter.X)

        #self.original_image = PhotoImage(self.oringinal_image.resize(), file="photoes/original.png").subsample(3)
        #self.view = ttk.Label(self.local_stack.get(), image=self.original_image, style="Image.TLabel")
        #self.view.pack()

        self.header_date_head = ttk.Label(self.local_stack.get(),
                                          text=self.language.get_text('date'),
                                          style="Header.TLabel")  # date (откуда брать дату)
        self.header_date_head.pack(fill=tkinter.X)

        self.header_date = ttk.Label(self.local_stack.get(),
                                     text=self.chart.get_date() if self.chart.get_date() else "-пусто-",
                                     style="Text.TLabel")  # date (откуда брать дату)
        self.header_date.pack(padx=10, pady=10, fill=tkinter.X)

        self.header_priority_head = ttk.Label(self.local_stack.get(),
                                              text=self.language.get_text('priority'),
                                              style="Header.TLabel")  # priority (диаграммы еще нет)
        self.header_priority_head.pack(fill=tkinter.X)

        self.header_priority = ttk.Label(self.local_stack.get(),
                                         text=self.chart.get_priority() if self.chart.get_priority() else "-пусто-",
                                         style="Text.TLabel")  # priority (диаграммы еще нет)
        self.header_priority.pack(padx=10, pady=10)

    def update_view(self, event):
        self.chart.double_click_left(event)
        self.header_view.configure(text=self.chart.get_header() if self.chart.get_header() else "-пусто-")
        self.node_text_label.configure(text=self.chart.get_text() if self.chart.get_text() else "-пусто-")
        if self.chart.get_date():
            date = self.chart.get_date()
            if self.language.language == 'english':
                year = int(date.split("/")[2])
                month = int(date.split("/")[0])
                day = int(date.split("/")[1])
                date = str(date[1]) + '/' + str(date[0]) + '/' + str(date[2])
            elif self.language.language == 'russian':
                year = int(date.split(".")[2])
                month = int(date.split(".")[1])
                day = int(date.split(".")[0])
                date = str(date[0]) + '.' + str(date[1]) + '.' + str(date[2])
        else:
            date = '-пусто-'
        self.header_date.configure(text=date)
        self.header_priority.configure(text=self.chart.get_priority() if self.chart.get_priority() else "-пусто-")
    def back(self):
        self.smw.pop()


#при нажатии на узел должен открываться фрейм со всем описанием узла выше(когда уже диаграмма будет добавлена на эту страницу нужно будет обработать нажатии на узел)

"""root = tkinter.Tk()
smw = stack_menu.StackMenuWidget(root)
first_page = ChartsViewPageWindow(root, smw,"123")
root.mainloop()"""

