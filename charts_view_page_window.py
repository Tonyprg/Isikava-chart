from tkinter import *
import tkinter
from tkinter import ttk
import stack_menu
import charts_view_and_edit_page_window as sf
from PIL import Image
import tree
import datetime
from PIL import Image, ImageTk
from textwrap import wrap
import files
import os

class ChartsViewPageWindow:
    def __init__(self, master, smw, chart_name, style, language):
        self.master = master
        self.smw = smw
        self.chart_name = chart_name
        self.style = style
        self.language = language

        self.smw.get().configure(style="BG.TFrame")
        self.smw.get().bind('<Configure>', self.on_resize)

        self.left_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")
        self.left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.chart = tree.Chart(self.left_frame, chart_name)
        if os.path.exists('charts/' + self.chart_name):
            self.chart.read_file('charts/' + self.chart_name)
        else:
            file = open('charts/' + self.chart_name, "w")
            file.close()
            self.chart.write_file('charts/' + self.chart_name)

        self.chart.field.canvas.bind("<Double-ButtonPress-1>", self.update_view)
        self.chart.field.canvas.unbind("<Double-ButtonPress-3>")

        self.back_button = ttk.Button(self.left_frame, text=self.language.get_text('back'), command=self.back, style="Btn.TButton")
        self.back_button.pack(side=tkinter.BOTTOM, anchor="sw", padx=10, pady=10)

        self.right_frame = ttk.Frame(self.smw.get(), style="Container.TFrame", width=self.smw.root.winfo_width()//4)
        self.right_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=False)

        self.canvas = Canvas(self.right_frame, bg=self.style.bg_color, width=self.smw.root.winfo_width()//4, height=self.smw.root.winfo_height())
        self.hbar = Scrollbar(self.right_frame, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = Scrollbar(self.right_frame, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=self.smw.root.winfo_width()//4, height=self.smw.root.winfo_height())
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.pack(anchor='n', fill=tkinter.BOTH)

        self.local_stack = stack_menu.StackMenuWidget(self.right_frame)
        self.local_stack.get().configure(style="SubMenu.TFrame")
        self.local_stack.stack.pop()
        self.local_stack.stack.append(self.canvas)

        self.build()

    def on_resize(self, event):
        self.smw.root.update()
        self.canvas.configure(height=self.smw.root.winfo_height())
    def _on_mousewheel(self, event):
        if event.x <= self.smw.root.winfo_width()//4:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_view(self, event):
        self.chart.double_click_left(event)
        self.canvas.delete('all')
        self.smw.root.update()
        self.build()

    def build(self):
        self.smw.root.update()
        height = 10
        self.header_view_head = ttk.Label(self.local_stack.get(),
                                          text=self.language.get_text('header'),
                                          style="Header.TLabel")
        self.header_view_head.pack(fill=tkinter.X)
        header_view_head_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                            window=self.header_view_head)
        self.smw.root.update()
        height += 56

        self.header_view = ttk.Label(self.local_stack.get(),
                                     text=self.chart.get_header() if self.chart.get_header() else self.language.get_text('empty'),
                                     style="Text.TLabel")
        self.header_view.pack(padx=10, pady=10, fill=tkinter.X)
        header_view_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                       window=self.header_view)
        self.smw.root.update()
        height += 56

        self.node_text_label_head = ttk.Label(self.local_stack.get(),
                                              text=self.language.get_text('content'),
                                              style="Header.TLabel")  # text (откуда брать текст)
        self.node_text_label_head.pack(fill=tkinter.X)
        node_text_label_head_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                                window=self.node_text_label_head)
        self.smw.root.update()
        height += 56

        self.node_text_label = ttk.Label(self.local_stack.get(),
                                         text=self.chart.get_text() if self.chart.get_text() else self.language.get_text('empty'),
                                         style="Text.TLabel")  # text (откуда брать текст)
        self.node_text_label.pack(padx=10, pady=10, fill=tkinter.X)
        self.smw.root.update()
        width = self.node_text_label.winfo_width()
        self.canvas.configure(width=self.smw.root.winfo_width() // 4)
        if width > self.smw.root.winfo_width() // 4:
            char_width = 14
            wrapped_text = '\n'.join(wrap(self.chart.get_text(), int(self.smw.root.winfo_width() // 4 / char_width)))
            self.node_text_label['text'] = wrapped_text
        node_text_label_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                           window=self.node_text_label)
        self.smw.root.update()
        height += self.node_text_label.winfo_height() + 10

        self.original_image_head = ttk.Label(self.local_stack.get(),
                                              text=self.language.get_text('image'),
                                              style="Header.TLabel")  # text (откуда брать текст)
        self.original_image_head.pack(fill=tkinter.X)
        node_text_label_head_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                                window=self.original_image_head)
        self.smw.root.update()
        height += 56

        if self.chart.get_image() and os.path.exists(self.chart.get_image()):
            im = Image.open(self.chart.get_image() + "/" + "original.png")
            width, img_height = im.size
            if width >= self.smw.root.winfo_width()//4:
                i = 1
                while width / i > self.smw.root.winfo_width()//4:
                    i += 1
                sub = i
            else:
                sub = 2
            self.original_image = PhotoImage(file=self.chart.get_image() + "/" + "original.png").subsample(sub)

            self.original_image_view = ttk.Label(self.local_stack.get(),
                                  image=self.original_image,
                                  style="Image.TLabel")
            self.original_image_view.pack(padx=10, pady=10, fill=tkinter.X)
            node_text_label_head_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                                    window=self.original_image_view)
            self.smw.root.update()
            height += self.original_image.height() + 10
        else:
            self.original_image_view = ttk.Label(self.local_stack.get(),
                                               text=self.language.get_text('empty'),
                                               style="Image.TLabel")
            self.original_image_view.pack(padx=10, pady=10, fill=tkinter.X)
            node_text_label_head_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                                    window=self.original_image_view)
            self.smw.root.update()
            height += 56

        self.header_date_head = ttk.Label(self.local_stack.get(),
                                          text=self.language.get_text('date'),
                                          style="Header.TLabel")  # date (откуда брать дату)
        self.header_date_head.pack(fill=tkinter.X)
        header_date_head_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                            window=self.header_date_head)
        self.smw.root.update()
        height += 56

        date = self.chart.get_date()
        if date:
            if '.' in date:
                if self.language.language == 'english':
                    year = date.split(".")[2]
                    month = date.split(".")[0]
                    day = date.split(".")[1]
                    date = str(day) + '/' + str(month) + '/' + str(year)
                elif self.language.language == 'russian':
                    year = date.split(".")[2]
                    month = date.split(".")[1]
                    day = date.split(".")[0]
                    date = str(day) + '.' + str(month) + '.' + str(year)
            elif '/' in date:
                if self.language.language == 'english':
                    year = date.split("/")[2]
                    month = date.split("/")[0]
                    day = date.split("/")[1]
                    date = str(day) + '/' + str(month) + '/' + str(year)
                elif self.language.language == 'russian':
                    year = date.split("/")[2]
                    month = date.split("/")[1]
                    day = date.split("/")[0]
                    date = str(day) + '.' + str(month) + '.' + str(year)
            else:
                date = ''

        self.header_date = ttk.Label(self.local_stack.get(),
                                     text=date if date else self.language.get_text('empty'),
                                     style="Text.TLabel")  # date (откуда брать дату)
        self.header_date.pack(padx=10, pady=10, fill=tkinter.X)
        header_date_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                       window=self.header_date)
        self.smw.root.update()
        height += 56

        self.header_priority_head = ttk.Label(self.local_stack.get(),
                                              text=self.language.get_text('priority'),
                                              style="Header.TLabel")  # priority (диаграммы еще нет)
        self.header_priority_head.pack(fill=tkinter.X)
        header_priority_head_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                                window=self.header_priority_head)
        self.smw.root.update()
        height += 56

        self.header_priority = ttk.Label(self.local_stack.get(),
                                         text=self.chart.get_priority() if self.chart.get_priority() else self.language.get_text('empty'),
                                         style="Text.TLabel")  # priority (диаграммы еще нет)
        self.header_priority.pack(padx=10, pady=10)
        header_priority_window = self.canvas.create_window(self.smw.root.winfo_width() // 8, height, anchor=N,
                                                           window=self.header_priority)
        self.smw.root.update()
        height += 56

        self.canvas.yview_moveto(0)
        self.canvas.configure(scrollregion=(0, 0, self.canvas.winfo_width(), height))

    def back(self):
        self.smw.pop()


#при нажатии на узел должен открываться фрейм со всем описанием узла выше(когда уже диаграмма будет добавлена на эту страницу нужно будет обработать нажатии на узел)

"""root = tkinter.Tk()
smw = stack_menu.StackMenuWidget(root)
first_page = ChartsViewPageWindow(root, smw,"123")
root.mainloop()"""

