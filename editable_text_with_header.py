import tkinter
from tkinter import ttk
from tkinter import scrolledtext

# фрейм с заголовком и редактируемым текстом
class EditableTextWithHeader:

    def __init__(self, root, text, header, smw, style, language):
        self.root = root
        self.text = text
        self.header = header
        self.smw = smw
        self.style = style
        self.language = language

        self.smw.get().configure(style="BG.TFrame")

        self.frame = ttk.Frame(self.root, style="Container.TFrame")
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        self.header = ttk.Label(self.frame, text=self.header, style="Header.TLabel")
        self.header.pack(padx=10, pady=10)

        self.text_field = scrolledtext.ScrolledText(self.frame, wrap="word",
                                                    width=int(self.smw.root.winfo_width()*0.25),
                                                    height=int(self.smw.root.winfo_width()*0.05))
        self.text_field.insert("1.0", self.text)
        self.text_field.pack(fill=tkinter.BOTH, padx=10, pady=10)

        self.btn_back = ttk.Button(
            self.frame,
            text=self.language.get_text('save'),
            command=lambda: self.back(),
            style="Btn.TButton")
        self.btn_back.pack(padx=10, pady=10)

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def back(self):
        s = self.text_field.get("1.0", tkinter.END)
        if len(s) != 1:
            while len(s) > 1 and s[-1] == '\n':
                s = s[:-1]
            if s == '\n':
                s = ''
        else:
            s = ''
        self.set_text(s)
        self.smw.pop()
