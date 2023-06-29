import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import files
import stack_menu
import settings_page_window as s
import charts_selection_page_window as ss
import styles
import languages
# import widgets as wd

class FrontPageNameWindow():
    def __init__(self, root, smw):
        self.root = root
        self.smw = smw

        self.style = styles.StyleManager()

        self.bg_label = ttk.Label(self.smw.get())
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.smw.get().bind("<Configure>", self.on_resize)

        self.language = languages.Language()

        settings = files.get_settings()
        if not settings:
            settings = dict()
        if 'language' not in settings.keys():
            settings['language'] = 'russian'
        if 'style' not in settings.keys():
            settings['style'] = 'dark'
        if settings['language'] == 'russian':
            self.language.set_language('russian')
        elif settings['language'] == 'english':
            self.language.set_language('english')
        if settings['style'] == 'light':
            self.style.set_style_one()
        elif settings['style'] == 'dark':
            self.style.set_style_two()

        self.smw.get().configure(style="BG.TFrame")

        # self.team_name = ttk.Label(self.smw.get(), text=self.language.get_text('team_name'),
        #                            style="Header.TLabel")
        # self.team_name.place(x=10, y=10)

        self.button_frame = ttk.Frame(self.smw.get(), style="Container.TFrame")  # Create a frame for buttons
        self.button_frame.place(relx=0.5, rely=0.5, anchor='center')

        # self.charts_button = wd.RoundedButton(master=self.button_frame, text=self.language.get_text('to_choose_chart_btn'),
        #                                       radius=40,
        #                                       btnbackground="#0078ff",
        #                                       btnforeground="#ffffff",
        #                                       width=100,
        #                                       height=100,
        #                                       clicked=self.charts)
        # self.charts_button.pack(expand=True, fill="both")

        self.charts_button = ttk.Button(
            self.button_frame, text=self.language.get_text('to_choose_chart_btn'),
            command=lambda: self.charts(), style="Btn.TButton")
        self.charts_button.pack(padx=10, pady=10)

        self.settings_button = ttk.Button(
            self.button_frame, text=self.language.get_text('to_settings_btn'), command=lambda: self.to_settings(), style="Btn.TButton")
        self.settings_button.pack(padx=10, pady=10)

        self.exit_button = ttk.Button(
            self.button_frame, text=self.language.get_text('exit_btn'), command=lambda: self.close(), style="Btn.TButton")
        self.exit_button.pack(padx=10, pady=10)

    # Функция, которая будет вызываться при изменении размера окна
    def on_resize(self, event = None):
        self.bg_raw = Image.open(self.style.bg)
        self.bg_raw_resized = self.bg_raw.resize((self.smw.get().winfo_width(), self.smw.get().winfo_height()))
        self.bg_image = ImageTk.PhotoImage(self.bg_raw_resized)
        self.bg_label.configure(image=self.bg_image)

    def charts(self):
        self.smw.push()
        chart_selection_page_window = ss.ChartsSelectionPageWindow(smw.get(), smw, self.style, self.language)

    def to_settings(self):
        self.smw.push()
        settings_window = s.SettingsWindow(smw.get(), smw, self.style, self.language, self)

    def close(self):
        smw.get()
        root.destroy()


root = tkinter.Tk()
root.geometry(str(int(root.winfo_screenwidth()*0.75))+'x'+str(int(root.winfo_screenheight()*0.75)))

smw = stack_menu.StackMenuWidget(root)

first_page = FrontPageNameWindow(root, smw)
root.mainloop()

#изменить сохранение картинок, заблокировать смену узлов при редактировании узла