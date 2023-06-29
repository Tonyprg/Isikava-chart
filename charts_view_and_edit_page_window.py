import tkinter
from tkinter import ttk
import stack_menu
import charts_edit_page_window as cepw
import charts_view_page_window as sf
from PIL import Image, ImageTk

class ChartsViewAndEditPageWindow():
    def __init__(self, master, smw, chart_name, style, language):
        self.chart_name = chart_name
        self.master = master
        self.smw = smw
        self.style = style
        self.language = language

        self.bg_label = ttk.Label(self.smw.get())
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.smw.get().bind("<Configure>", self.on_resize)

        smw.get().configure(style="BG.TFrame")

        self.button_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")
        self.button_frame.pack(expand=1)

        self.view_a_chart_button = ttk.Button(self.button_frame, text=self.language.get_text('view'), command=self.view, style="Btn.TButton")
        self.view_a_chart_button.pack(padx=10, pady=10)

        self.edit_a_chart_button = ttk.Button(self.button_frame, text=self.language.get_text('edit'), command=self.edit, style="Btn.TButton")
        self.edit_a_chart_button.pack(padx=10, pady=10)

        self.back_button = ttk.Button(self.button_frame, text=self.language.get_text('back'), command=self.back, style="Btn.TButton")
        self.back_button.pack(padx=10, pady=10)

    # Функция, которая будет вызываться при изменении размера окна
    def on_resize(self, event):
        self.bg_raw = Image.open(self.style.bg)
        self.bg_raw_resized = self.bg_raw.resize((self.smw.get().winfo_width(), self.smw.get().winfo_height()))
        self.bg_image = ImageTk.PhotoImage(self.bg_raw_resized)
        self.bg_label.configure(image=self.bg_image)

    def view(self):
        self.smw.push()
        charts_view_page_window = sf.ChartsViewPageWindow(self.smw.get(), self.smw, self.chart_name, self.style, self.language)


    def edit(self):
        self.smw.push()
        charts_edit_page_window = cepw.ChartsEditPageWindow(self.smw.get(), self.smw, self.chart_name, self.style, self.language)


    def back(self):
        self.smw.pop()

##root = tkinter.Tk()
##smw = stack_menu.StackMenuWidget(root)
##Chach = ChartsViewAndEditPageWindow(root,smw)
##root.mainloop()







