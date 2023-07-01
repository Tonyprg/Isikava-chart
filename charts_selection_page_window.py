import tkinter
from tkinter import ttk
import stack_menu
import files
import charts_view_and_edit_page_window as cvaepw
import styles
import tree
from PIL import Image, ImageTk
import os
import shutil

class ChartsSelectionPageWindow:
    def __init__(self, master, smw, style, language):
        self.master = master
        self.smw = smw
        self.style = style
        self.language = language

        self.bg_label = ttk.Label(self.smw.get())
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.smw.get().bind("<Configure>", self.on_resize)

        smw.get().configure(style="BG.TFrame")

        self.center_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")
        self.center_frame.pack(expand=1)

        self.chart_input = ttk.Frame(self.center_frame, style="Container.TFrame")
        self.chart_input.pack(padx=10, pady=10)

        self.chart_name_entry = ttk.Entry(self.chart_input, validate='all', justify='center', style="Entry.TEntry",
                                          font = ('helvetica', 14))
        vcmd = (self.chart_name_entry.register(self.check_len))
        self.chart_name_entry.configure(validatecommand=(vcmd, '%P'))
        self.chart_name_entry.pack(side=tkinter.LEFT, padx=10, pady=10)

        self.add_chart_button = ttk.Button(self.chart_input, text=self.language.get_text('add_chart'), command=self.add, style="Btn.TButton")
        self.add_chart_button.pack(side=tkinter.RIGHT, padx=10, pady=10)

        self.list_frame = ttk.Frame(self.center_frame, style="Container.TFrame")
        self.list_frame.pack(fill=tkinter.X, padx=10, pady=10)

        self.chart_selection_list_scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical")

        self.chart_selection_list = ttk.Treeview(self.list_frame,
                                                 yscrollcommand=self.chart_selection_list_scrollbar.set, show="tree",
                                                 style="Listbox.Treeview")

        self.chart_selection_list_scrollbar.config(command=self.chart_selection_list.yview)

        self.chart_select = []
        save_file = files.get_text_from_file("charts.txt").split("\n")
        for element in save_file:
            if element:
                self.chart_selection_list.insert("", len(self.chart_select), text=element)
                self.chart_select.append(element)

        self.chart_selection_list_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.chart_selection_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.chart_do = ttk.Frame(self.center_frame, style="Container.TFrame")
        self.chart_do.pack(padx=10, pady=10)

        self.choose_chart_button = ttk.Button(self.chart_do, text=self.language.get_text('choose_chart'), command=self.on_chart_choose, style="Btn.TButton")
        self.choose_chart_button.pack(side=tkinter.LEFT, padx=10, pady=10)

        self.del_chart_button = ttk.Button(self.chart_do, text=self.language.get_text('delete_chart'), command=self.delete, style="Btn.TButton")
        self.del_chart_button.pack(side=tkinter.LEFT, padx=10, pady=10)

        self.back_button = ttk.Button(self.center_frame, text=self.language.get_text('back'), command=self.back, style="Btn.TButton")
        self.back_button.pack(padx=10, pady=10)

    # Функция, которая будет вызываться при изменении размера окна
    def on_resize(self, event):
        self.bg_raw = Image.open(self.style.bg)
        self.bg_raw_resized = self.bg_raw.resize((self.smw.get().winfo_width(), self.smw.get().winfo_height()))
        self.bg_image = ImageTk.PhotoImage(self.bg_raw_resized)
        self.bg_label.configure(image=self.bg_image)

    def on_chart_choose(self):
        self.chart_name_entry.delete(0, tkinter.END)
        cur_item = self.chart_selection_list.item(self.chart_selection_list.focus())
        if cur_item['text']:
            chart_name = cur_item['text']
            self.smw.push()
            charts_view_and_edit_page_window = cvaepw.ChartsViewAndEditPageWindow(self.smw.get(), self.smw, chart_name,
                                                                                  self.style, self.language)


    def delete(self):
        cur_item = self.chart_selection_list.item(self.chart_selection_list.focus())
        if cur_item['text']:
            self.chart_selection_list.delete(self.chart_selection_list.selection()[0])
            del self.chart_select[self.chart_select.index(cur_item['text'])]
            self.save()
            if os.path.exists('charts/' + cur_item['text']):
                os.remove('charts/' + cur_item['text'])
            if os.path.exists('photoes/' + cur_item['text']):
                shutil.rmtree('photoes/' + cur_item['text'])

    # добавление нового элемента
    def add(self):
        new_chart = self.chart_name_entry.get()

        charts_file = open('charts.txt','r').read()
        if new_chart not in (charts_file.split('\n')) and new_chart:
            while new_chart.find("  ") != -1:
                new_chart = new_chart[:new_chart.find("  ")] + new_chart[new_chart.find("  ")+1:]
            if len(new_chart) >= 1 and new_chart[0] == " ":
                new_chart = new_chart[1:]
            if len(new_chart) >= 1 and new_chart[-1] == " ":
                new_chart = new_chart[:-1]

            self.chart_name_entry.delete(0, tkinter.END)

            if not os.path.exists("charts"):
                os.makedirs("charts")
            frm = ttk.Frame()
            chart = tree.Chart(frm, name=new_chart)
            chart.write_file('charts/'+new_chart)
            del chart
            del frm
            if new_chart:
                self.chart_selection_list.insert("", len(self.chart_select), text=new_chart)
                self.chart_select.append(new_chart)
                self.save()

    def save(self):
        save = ""
        for element in self.chart_select:
            save = save + element+"\n"
        files.input_text_to_file("charts.txt", save)

    def check_len(self, P):

        if len(P) <= 20:
            return True
        else:
            return False

    def back(self):
        self.smw.pop()
