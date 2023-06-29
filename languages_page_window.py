from tkinter import *
import tkinter
from tkinter import ttk
import stack_menu
import styles
from PIL import Image, ImageTk
import files

class LanguagesWindow():
    def __init__(self, root, smw, style, language, settings_page, front_page):
        self.root = root
        self.smw = smw
        self.style = style
        self.front_page = front_page
        self.settings_page = settings_page

        self.language=language

        self.bg_label = ttk.Label(self.smw.get())
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.smw.get().bind("<Configure>", self.on_resize)

        smw.get().configure(style="BG.TFrame")

        self.button_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")
        self.russian_button = ttk.Button(
        self.button_frame, text=self.language.get_text('ru_language'), command=lambda: self.lang_change('russian'), style="Btn.TButton")
        self.russian_button.pack(padx=10, pady=10)

        self.english_button = ttk.Button(
        self.button_frame, text=self.language.get_text('eng_language'), command=lambda: self.lang_change('english'), style="Btn.TButton")
        self.english_button.pack(padx=10, pady=10)



        self.back_button = ttk.Button(
           self.button_frame, text=self.language.get_text('back'), command=lambda: self.back(root, smw), style="Btn.TButton")
        self.back_button.pack(padx=10, pady=10)
        self.button_frame.pack(expand=1)

    def on_resize(self, event = None):
        self.bg_raw = Image.open(self.style.bg)
        self.bg_raw_resized = self.bg_raw.resize((self.smw.get().winfo_width(), self.smw.get().winfo_height()))
        self.bg_image = ImageTk.PhotoImage(self.bg_raw_resized)
        self.bg_label.configure(image=self.bg_image)

    def lang_change(self, lang):
        self.language.set_language(lang)

        settings = files.get_settings()
        if not settings:
            settings = dict()
        if lang == 'russian':
            settings['language'] = 'russian'
            files.save_settings(settings)
        elif lang == 'english':
            settings['language'] = 'english'
            files.save_settings(settings)

        self.smw.pop()
        self.smw.push()
        language_window = LanguagesWindow(self.smw.get(), self.smw, self.style, self.language, self.settings_page, self.front_page)

        self.front_page.team_name.configure(text=self.language.get_text('team_name'))
        self.front_page.charts_button.configure(text=self.language.get_text('to_choose_chart_btn'))
        self.front_page.settings_button.configure(text=self.language.get_text('to_settings_btn'))
        self.front_page.exit_button.configure(text=self.language.get_text('exit_btn'))

        self.settings_page.styles.configure(text=self.language.get_text('change_style'))
        self.settings_page.languages.configure(text=self.language.get_text('change_language'))
        self.settings_page.back_button.configure(text=self.language.get_text('back'))
    
    def back(self, root, smw):
        self.smw.pop()
        
        



