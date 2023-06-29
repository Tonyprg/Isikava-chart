from tkinter import *
import tkinter
from tkinter import ttk
import stack_menu
import styles_page_window as s
import languages_page_window as ss
from PIL import Image, ImageTk


class SettingsWindow():
    def __init__(self, root, smw, style, language, front_page):
        self.root = root
        self.smw = smw
        self.style = style
        self.front_page = front_page
        self.language = language

        self.bg_label = ttk.Label(self.smw.get())
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.smw.get().bind("<Configure>", self.on_resize)

        smw.get().configure(style="BG.TFrame")

        self.button_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")

        self.styles = ttk.Button(
            self.button_frame, text=self.language.get_text('change_style'), command=lambda: self.change_style_window(), style="Btn.TButton")
        self.styles.pack(padx=10, pady=10)

        self.languages = ttk.Button(
            self.button_frame, text=self.language.get_text('change_language'), command=lambda: self.change_language(), style="Btn.TButton")
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

    def change_style_window(self):
        self.smw.push()
        styles_window = s.StylesWindow(self.smw.get(), self.smw, self.style, self.language, self.front_page, self)

    def change_language(self):
        self.smw.push()
        language_window = ss.LanguagesWindow(self.smw.get(), self.smw, self.style, self.language, self, self.front_page)

    # def styles(self,root,smw): работа для юли

    def back(self, root, smw):
        self.smw.pop()





