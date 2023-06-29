import calendar
import tkinter
from tkinter import ttk
import files
import stack_menu
import editable_date_with_header
import editable_text_with_header
import image_editor
import tree
import datetime
from PIL import Image, ImageTk

class ChartsEditPageWindow:
        def __init__(self, master, smw, chart_name, style, language):
            self.master = master
            self.smw = smw
            self.chart_name = chart_name
            self.style = style
            self.language = language

            smw.get().configure(style="BG.TFrame")

            self.left_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")
            self.left_frame.pack(anchor=tkinter.W, side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

            self.chart = tree.Chart(self.left_frame, chart_name)
            self.chart.read_file('charts\\' + self.chart_name)

            self.back_button = ttk.Button(self.left_frame, text=self.language.get_text('back'), command=self.back, style="Btn.TButton")
            self.back_button.pack(side=tkinter.LEFT, anchor="sw", padx=10, pady=10)

            self.right_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")
            self.right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=False)

            self.local_stack = stack_menu.StackMenuWidget(self.right_frame)
            self.local_stack.get().configure(style="SubMenu.TFrame")

            self.edit_node = ttk.Label(self.local_stack.get(),
                                       text=self.language.get_text('node'),
                                       style="HeaderBorderless.TLabel")
            self.edit_node.pack(padx=10, pady=10)

            self.node_frame = ttk.Frame(self.local_stack.get(), style="Container.TFrame")
            self.node_frame.pack(fill=tkinter.BOTH, padx=10, pady=10)

            self.header_edit_button = ttk.Button(self.node_frame, text=self.language.get_text('edit_header'),
                                                 command=self.head_edit, style="Btn.TButton")
            self.header_edit_button.pack(padx=10, pady=10)

            self.text_edit_button = ttk.Button(self.node_frame, text=self.language.get_text('edit_content'),
                                               command=self.text_edit, style="Btn.TButton")
            self.text_edit_button.pack(padx=10, pady=10)

            self.image_edit_button = ttk.Button(self.node_frame, text=self.language.get_text('edit_image'),
                                                command=self.image_edit, style="Btn.TButton")
            self.image_edit_button.pack(padx=10, pady=10)

            self.date_edit_button = ttk.Button(self.node_frame, text=self.language.get_text('edit_date'),
                                               command=self.date_edit, style="Btn.TButton")
            self.date_edit_button.pack(padx=10, pady=10)

            self.priority_edit_button = ttk.Button(self.node_frame, text=self.language.get_text('edit_priority'),
                                                   command=self.priority_edit, style="Btn.TButton")
            self.priority_edit_button.pack(padx=10, pady=10)

            self.edit_chart = ttk.Label(self.local_stack.get(),
                                       text=self.language.get_text('chart'),
                                       style="HeaderBorderless.TLabel")
            self.edit_chart.pack(padx=10, pady=10)

            self.chart_frame = ttk.Frame(self.local_stack.get(), style="Container.TFrame")
            self.chart_frame.pack(fill=tkinter.BOTH, padx=10, pady=10)

            self.add_node_button = ttk.Button(self.chart_frame, text=self.language.get_text('add_node'),
                                              command=self.chart.append_node, style="Btn.TButton")
            self.add_node_button.pack(padx=10, pady=10)

            self.del_node_button = ttk.Button(self.chart_frame, text=self.language.get_text('del_node'),
                                              command=self.chart.remove_node, style="Btn.TButton")
            self.del_node_button.pack(padx=10, pady=10)

            self.style_edit_button = ttk.Button(self.chart_frame, text=self.language.get_text('edit_chart_style'),
                                                command=self.style_edit, style="Btn.TButton")
            self.style_edit_button.pack(padx=10, pady=10)

        def style_edit(self):
            self.local_stack.push()
            self.local_stack.get().configure(style="SubMenu.TFrame")

        def head_edit(self):
            self.local_stack.push()
            self.local_stack.get().configure(style="SubMenu.TFrame")

            header = ttk.Label(self.local_stack.get(), text=self.language.get_text('header'), style="Header.TLabel")
            header.pack(padx=10, pady=10)

            insert = ttk.Entry(self.local_stack.get(), validate='all', justify='center', style="Entry.TEntry",
                               font = ('helvetica', 14))
            if self.chart.get_header():
                insert.insert("0", self.chart.get_header())
            vcmd = (insert.register(self.check_len))
            insert.configure(validatecommand=(vcmd, '%P'))
            insert.pack(fill=tkinter.X, padx=10, pady=10)

            back = ttk.Button(self.local_stack.get(), text=self.language.get_text('save'), style="Btn.TButton")
            back.configure(command=lambda: self.save_header(insert))
            back.pack(padx=10, pady=10)


        def text_edit(self):
            self.local_stack.push()
            self.local_stack.get().configure(style="SubMenu.TFrame")
            edit = editable_text_with_header.EditableTextWithHeader(self.local_stack.get(),
                                                                    self.chart.get_text() if self.chart.get_text() else "",
                                                                    self.language.get_text('content'), self.local_stack,
                                                                    self.style, self.language)
            edit.btn_back.configure(command=lambda: self.save_text(edit))

        def image_edit(self):
            self.local_stack.push()
            self.local_stack.get().configure(style="SubMenu.TFrame")
            image = image_editor.ImageEditor(self.local_stack.get(), self.local_stack)

        def date_edit(self):
            self.local_stack.push()
            self.local_stack.get().configure(style="SubMenu.TFrame")
            if self.language.language == 'english':
                today = str(datetime.date.today().month) + '/' + str(datetime.date.today().day) + '/' + str(datetime.date.today().year)
            elif self.language.language == 'russian':
                today = str(datetime.date.today().day) + '.' + str(datetime.date.today().month) + '.' + str(
                    datetime.date.today().year)
            edit = editable_date_with_header.EditableDateWithHeader(self.local_stack.get(),
                                                                    self.chart.get_date() if self.chart.get_date() else today,
                                                                    self.language.get_text('date'), self.local_stack,
                                                                    self.style, self.language)
            edit.btn_back.configure(command=lambda: self.save_date(edit))


        def priority_edit(self):
            self.local_stack.push()
            self.local_stack.get().configure(style="SubMenu.TFrame")

            header = ttk.Label(self.local_stack.get(), text=self.language.get_text('priority'), style="Header.TLabel")
            header.pack(padx=10, pady=10)

            insert = ttk.Entry(self.local_stack.get(), validate='all', justify='center', style="Entry.TEntry",
                               font = ('helvetica', 14))
            if self.chart.get_priority():
                insert.insert("0", self.chart.get_priority())
            vcmd = (insert.register(self.check_digit))
            insert.configure(validatecommand=(vcmd, '%P'))
            insert.pack(fill=tkinter.X, padx=10, pady=10)

            back = ttk.Button(self.local_stack.get(), text=self.language.get_text('save'), style="Btn.TButton")
            back.configure(command=lambda: self.save_priority(insert))
            back.pack(padx=10, pady=10)


        def save_header(self, insert):
            self.chart.set_header(insert.get())
            self.chart.write_file('charts\\' + self.chart_name)
            self.local_stack.pop()
            self.chart.field.redraw()



        def save_text(self, edit):
            edit.back()
            self.chart.set_text(edit.get_text())
            self.chart.write_file('charts\\' + self.chart_name)



        def save_date(self, edit):
            edit.back()
            self.chart.set_date(edit.get_date())
            self.chart.write_file('charts\\' + self.chart_name)



        def save_priority(self, insert):
            self.chart.set_priority(insert.get())
            self.chart.write_file('charts\\' + self.chart_name)
            self.local_stack.pop()

        def check_digit(self, P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False

        def check_len(self, P):

            if len(P) <= 20:
                return True
            else:
                return False

        def back(self):
            self.chart.write_file('charts\\' + self.chart_name)
            self.smw.pop()
