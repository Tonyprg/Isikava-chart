from tkinter import ttk
class StyleManager:
    def __init__(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.set_font("helvetica 14")
    def set_font(self, font):
        self.style.configure(".",
                             font=font)


    def set_style_one(self):
        self.bg = 'bg_light.png'
        self.style.configure("BG.TFrame",
                             foreground="black",
                             padding=10,
                             background="lightgray")
        self.style.configure("Listbox.Treeview",
                             padding=10)
        self.style.configure("Container.TFrame",
                             foreground="black",
                             relief="ridge",
                             padding=10,
                             background="lightgray")
        self.style.configure("SubMenu.TFrame",
                             relief="ridge",
                             foreground="black",
                             padding=10,
                             background="lightgray")
        self.style.configure("Entry.TEntry",
                             foreground="black",
                             width=20,
                             padding=5,
                             background="white")
        self.style.configure("Header.TLabel",
                             anchor='center',
                             width=20,
                             relief="ridge",
                             foreground="black",
                             padding=10,
                             background="lightgray")
        self.style.configure("HeaderBorderless.TLabel",
                             anchor='center',
                             width=20,
                             foreground="black",
                             padding=10,
                             background="lightgray")
        self.style.configure("Text.TLabel",
                             anchor='center',
                             foreground="black",
                             padding=10,
                             background="lightgray")
        self.style.configure("Image.TLabel",
                             foreground="black",
                             padding=10,
                             background="lightgray")
        self.style.configure("Btn.TButton",
                             width=20,
                             borderwidth=1,
                             focusthickness=3,
                             focuscolor='none',
                             justify='center',
                             foreground="black",
                             padding=10,
                             background="white")

    def set_style_two(self):
        self.bg = 'bg_dark.png'
        self.style.configure("BG.TFrame",
                             foreground="lightgray",
                             padding=10,
                             background="#292b2f")
        self.style.configure("Listbox.Treeview",

                             padding=10)
        self.style.configure("Container.TFrame",
                             relief="ridge",
                             foreground="lightgray",
                             padding=10,
                             background="#292b2f")
        self.style.configure("SubMenu.TFrame",
                             relief="ridge",
                             foreground="lightgray",
                             padding=10,
                             background="#292b2f")
        self.style.configure("Entry.TEntry",
                             foreground="lightgray",
                             width=20,
                             padding=5,
                             background="#292b2f")
        self.style.configure("Header.TLabel",
                             anchor='center',
                             width=20,
                             relief="ridge",
                             foreground="lightgray",
                             padding=10,
                             background="#292b2f")
        self.style.configure("HeaderBorderless.TLabel",
                             anchor='center',
                             width=20,
                             foreground="lightgray",
                             padding=10,
                             background="#292b2f")
        self.style.configure("Text.TLabel",
                             anchor='center',
                             foreground="lightgray",
                             padding=10,
                             background="#292b2f")
        self.style.configure("Image.TLabel",
                             foreground="lightgray",
                             padding=10,
                             background="#292b2f")
        self.style.configure("Btn.TButton",
                             width=20,
                             borderwidth=1,
                             focusthickness=3,
                             focuscolor='none',
                             justify='center',
                             foreground="lightgray",
                             padding=10,
                             background="#292b2f")


