import tkinter
from tkinter import ttk
import tkcalendar

class EditableDateWithHeader:

    def __init__(self, root, date, header, smw, style, language):
        self.root = root
        self.date = date
        self.header = header
        self.style = style
        self.smw = smw
        self.language = language

        smw.get().configure(style="BG.TFrame")

        self.frame = ttk.Frame(self.root, style="Container.TFrame")
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        self.header = ttk.Label(self.frame, text=self.header, style="Header.TLabel")
        self.header.pack(padx=10, pady=10)

        if self.date:
            if self.language.language == 'english':
                year = int(self.date.split("/")[2])
                month = int(self.date.split("/")[0])
                day = int(self.date.split("/")[1])
            elif self.language.language == 'russian':
                year = int(self.date.split(".")[2])
                month = int(self.date.split(".")[1])
                day = int(self.date.split(".")[0])


        self.calendar = tkcalendar.Calendar(self.frame,
                                            locale='ru_RU' if self.language.language == 'russian' else 'en_US',
                                            selectmode="day", year=year, month=month, day=day)
        self.calendar.pack(padx=10, pady=10)
        self.calendar.bind("<Leave>", lambda event, arg=self.frame: self.edited())

        self.btn_back = ttk.Button(
            self.frame,
            text=self.language.get_text('save'),
            command=lambda: self.back(),
            style="Btn.TButton")
        self.btn_back.pack(padx=10, pady=10)

    def edited(self):
        self.set_date(self.calendar.get_date())

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def back(self):
        self.smw.pop()
