from tkinter import *
import tkinter
from tkinter import ttk
import stack_menu
import styles
from PIL import Image, ImageTk
import files

class StylesWindow():
    def __init__(self, root, smw, style, language, front_page, settings_page):
        self.root = root
        self.smw = smw
        self.style = style
        self.language = language
        self.front_page = front_page
        self.settings_page = settings_page

        self.bg_label = ttk.Label(self.smw.get())
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.smw.get().bind("<Configure>", self.on_resize)

        smw.get().configure(style="BG.TFrame")

        self.button_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")

        self.styles = ttk.Button(
            self.button_frame, text=self.language.get_text('light_theme'),command=lambda: self.light(), style="Btn.TButton")
        self.styles.pack(padx=10, pady=10)

        self.languages = ttk.Button(
            self.button_frame, text=self.language.get_text('dark_theme'),command=lambda: self.dark(), style="Btn.TButton")
        self.languages.pack(padx=10, pady=10)
        
        self.back_button = ttk.Button(
            self.button_frame, text=self.language.get_text('back'), command=lambda: self.back(root, smw), style="Btn.TButton")
        self.back_button.pack(padx=10, pady=10)
        
        self.button_frame.pack(expand=1)

    def on_resize(self, event = None):
        self.bg_raw = Image.open(self.style.bg)
        self.bg_raw_resized = self.bg_raw.resize((self.smw.get().winfo_width(), self.smw.get().winfo_height()))
        self.bg_image = ImageTk.PhotoImage(self.bg_raw_resized)
        self.bg_label.configure(image=self.bg_image)

    def light(self):
        self.style.set_style_one()
        self.front_page.on_resize()
        self.settings_page.on_resize()
        self.on_resize()
        settings = files.get_settings()
        if not settings:
            settings = dict()
        settings['style'] = 'light'
        files.save_settings(settings)


    def dark(self):
        self.style.set_style_two()
        self.front_page.on_resize()
        self.settings_page.on_resize()
        self.on_resize()
        settings = files.get_settings()
        if not settings:
            settings = dict()
        settings['style'] = 'dark'
        files.save_settings(settings)
    
    #def styles(self,root,smw): работа для юли

        
    def back(self, root, smw):
        self.smw.pop()
        
        




