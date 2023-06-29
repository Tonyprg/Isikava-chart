import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
# from PIL import ImageGrab
import pyscreenshot as ImageGrab
from tkinter import messagebox
import math

class ImageEditor:
    def __init__(self, master, smw):
        self.master = master
        self.smw = smw
        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.image_frame, width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=False)

        self.image = None
        self.image_path = None
        self.crop_rect = None
        self.crop_shape = "rectangle"
        self.scale_factor = 1.0
        button_font = ("TkDefaultFont", 12)
        self.WIDTH=None
        self.HEIGHT=None

        self.load_button = tk.Button(self.control_frame, text="Загрузить изображение \n из буфера обмена", command=self.load_image, font=button_font)
        self.load_button.pack(anchor=tk.W)

        self.shape_size_label = tk.Label(self.control_frame, text="Размер:", font=button_font)
        self.shape_size_label.pack(pady=10, anchor=tk.W)

        self.scale_button = tk.Button(self.control_frame, text="Увеличить", command=self.scale_image_up, font=button_font)
        self.scale_button.pack(pady=10, anchor=tk.W)

        self.scale_button2 = tk.Button(self.control_frame, text="Уменьшить", command=self.scale_image_down, font=button_font)
        self.scale_button2.pack(pady=10, anchor=tk.W)

        self.shape_label = tk.Label(self.control_frame, text="Выбрать форму обрезки:", font=button_font)
        self.shape_label.pack(pady=10, anchor=tk.W)

        self.shape_frame = tk.Frame(self.control_frame)
        self.shape_frame.pack(pady=10, anchor=tk.W)

        self.circle_button = tk.Button(self.shape_frame, text="Круг", command=self.crop_image_circle, font=button_font)
        self.circle_button.pack(side=tk.LEFT)

        self.rectangle_button = tk.Button(self.shape_frame, text="Прямоугольник", command=self.crop_image, font=button_font)
        self.rectangle_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.control_frame, text="Сохранить изменения", command=self.save_changes, font=button_font)
        self.save_button.pack(pady=10, anchor=tk.W)

        self.control_frame.pack(side=tk.TOP, fill=tk.Y)

        self.shape_size_label = tk.Label(self.control_frame, text="Назад/Вперед:", font=button_font)
        self.shape_size_label.pack(pady=10, anchor=tk.W)

        self.undo_button = tk.Button(self.control_frame, text="<", command=self.undo_action, state=tk.DISABLED, font=button_font)
        self.undo_button.pack(side=tk.LEFT, pady=10, anchor=tk.W)

        self.redo_button = tk.Button(self.control_frame, text=">", command=self.redo_action, state=tk.DISABLED, font=button_font)
        self.redo_button.pack(side=tk.LEFT, pady=10, anchor=tk.W)

        self.image_up = 2
        self.image_down = 1
        self.undo_stack = []
        self.redo_stack = []

        self.update_undo_redo_buttons()
        
        self.scale_factor_ud = 0.9
        self.scale_step_ud = 0.1
        self.orig_image_for_scale_cropped=None
        self.size_of_orig = None
        self.return_image_back = None

    def load_image(self):
        clipboard_image = ImageGrab.grabclipboard()
        if clipboard_image:
            self.image = clipboard_image
            self.default_image = self.image
            self.size_of_orig = self.image
            self.WIDTH=self.image.width
            self.HEIGHT=self.image.height
            

            if self.WIDTH <= 600 and self.HEIGHT<=600:
                self.show_image()
                self.image = self.image
            else:
                while self.WIDTH >= 600 or self.HEIGHT>=600:
                        self.scale_factor = 0.9
                        self.WIDTH = int(self.WIDTH * self.scale_factor)
                        self.HEIGHT = int(self.HEIGHT * self.scale_factor)
                        self.image = self.image.resize((self.WIDTH, self.HEIGHT))
                        
                        self.show_image()
                        self.image = self.image
                    
                        
            ## wight- 1620  *  height -  2160
            self.orig_image_for_scale = self.image
            self.size_of_orig = self.image
            self.return_image_back = self.image
            
        else:
            messagebox.showerror("Ошибка", "Нет изображения в буфере обмена")

    def show_image(self):
        self.canvas.delete("all")
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)


    def crop_image(self):
        if self.image:
            self.canvas.config(cursor="crosshair")
            self.canvas.bind("<ButtonPress-1>", self.start_crop)
            self.canvas.bind("<B1-Motion>", self.draw_crop_rect)
            self.canvas.bind("<ButtonRelease-1>", self.end_crop)
            self.return_image_back = self.image
            

    def start_crop(self, event):
        self.crop_rect = [event.x, event.y, event.x, event.y]

    def draw_crop_rect(self, event):
        if self.crop_rect:
            self.canvas.delete("crop_rect")
            x1, y1, _, _ = self.crop_rect
            x2, y2 = min(event.x, self.image.width), min(event.y, self.image.height)


            x1 = max(x1, 0)
            x2 = min(x2, self.image.width)
            y1 = max(y1, 0)
            y2 = min(y2, self.image.height)

            self.crop_rect[2] = x2
            self.crop_rect[3] = y2

            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", tag="crop_rect")


    def end_crop(self, event):
        if self.crop_rect:
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            x1, y1, x2, y2 = self.crop_rect[0], self.crop_rect[1], event.x, event.y

            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1

            x1, x2 = max(x1, 0), min(x2, self.image.width)
            y1, y2 = max(y1, 0), min(y2, self.image.height)

            if x1 < x2 and y1 < y2:
                self.undo_stack.append(self.image.copy())
                self.redo_stack = []
                self.image = self.image.crop((x1, y1, x2, y2))
            self.crop_rect = None
            self.show_image()
            self.update_undo_redo_buttons()

            if self.image.width < 200 or self.image.height < 150:
                messagebox.showinfo("Внимание", "Выделенная область для обрезки слишком мала! Выделите еще раз")
                self.image = self.return_image_back
                self.show_image()
                self.crop_image
                
            else:
                self.return_image_back = self.image
                
            self.orig_image_for_scale = self.image
        self.scale_factor_ud=1
            
            


    def crop_image_circle(self):
        if self.image:
            self.canvas.config(cursor="crosshair")
            self.canvas.bind("<Button-1>", self.start_crop_circle)
            self.canvas.bind("<B1-Motion>", self.draw_crop_circle)
            self.canvas.bind("<ButtonRelease-1>", self.end_crop_circle)
            self.return_image_back = self.image

    def update_crop(self, event):
        self.canvas.delete("crop_shape")
        x0, y0 = self.crop_rect[0], self.crop_rect[1]
        x1, y1 = event.x, event.y
        radius = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        self.crop_rect = (x0 - radius, y0 - radius, x0 + radius, y0 + radius)
        self.canvas.create_oval(*self.crop_rect, outline="red", tag="crop_shape")

    def finish_crop(self, event):
        self.canvas.delete("crop_shape")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")


    def start_crop_circle(self, event):
        self.crop_rect = [event.x, event.y, event.x, event.y]

    def draw_crop_circle(self, event):
        if self.crop_rect:
            self.canvas.delete("crop_rect")
            x1, y1, _, _ = self.crop_rect
            x2, y2 = min(event.x, self.image.width), min(event.y, self.image.height)


            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            radius = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 2

            left = center_x - radius
            top = center_y - radius
            right = center_x + radius
            bottom = center_y + radius

            left = max(left, 0)
            right = min(right, self.image.width)
            top = max(top, 0)
            bottom = min(bottom, self.image.height)

            self.crop_rect[2] = x2
            self.crop_rect[3] = y2

            self.canvas.create_oval(left, top, right, bottom, outline="black", tag="crop_rect")


    def end_crop_circle(self, event):
        if self.crop_rect:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            x1, y1, x2, y2 = self.crop_rect[0], self.crop_rect[1], event.x, event.y

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            radius = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 2

            left = center_x - radius
            top = center_y - radius
            right = center_x + radius
            bottom = center_y + radius

            left, right = max(left, 0), min(right, self.image.width)
            top, bottom = max(top, 0), min(bottom, self.image.height)

            cropped_image = self.image.crop((left, top, right, bottom))

            circular_width = int(radius * 2)
            circular_height = int(radius * 2)

            cropped_image = cropped_image.resize((circular_width, circular_height))

            circular_image = Image.new("RGBA", (circular_width, circular_height), (0, 0, 0, 0))
            mask = Image.new("L", (circular_width, circular_height), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, circular_width, circular_height), fill=255)
            circular_image.paste(cropped_image, (0, 0), mask=mask)

            self.undo_stack.append(self.image.copy())
            self.redo_stack = []
            self.image = circular_image
            if self.image.width > 550 or self.image.height > 550:
                self.scale_factor = 0.5
                self.ww=None
                self.hh=None
                self.ww = int(self.image.width  * self.scale_factor)
                self.hh = int(self.image.height * self.scale_factor)
                self.image = self.image.resize((self.ww , self.hh))
                
                
           
            self.crop_rect = None
            self.show_image()
            self.update_undo_redo_buttons()

            if self.image.width < 200 or self.image.height < 150:
                messagebox.showinfo("Внимание", "Выделенная область для обрезки слишком мала! Выделите еще раз")
                self.image = self.return_image_back
                self.show_image()
                self.crop_image
                
            else:
                self.return_image_back = self.image
                
            self.orig_image_for_scale = self.image
        self.scale_step_ud = 0.1
        self.scale_factor_ud=1
    def scale_image_up(self):
        if self.orig_image_for_scale:
            self.undo_stack.append(self.image.copy())
            self.redo_stack = []
            if 0.98 <= (self.scale_factor_ud + self.scale_step_ud) <= 1.1:
                self.scale_factor_ud += self.scale_step_ud * 2
            else:
                self.scale_factor_ud += self.scale_step_ud
            

            if self.scale_factor_ud:
                w, h = self.orig_image_for_scale.size
                w = int(w * self.scale_factor_ud)
                h = int(h * self.scale_factor_ud)
                
                if w >= 550 or h >= 550:
                    messagebox.showinfo("Внимание", "Максимальный размер достигнут")
                    self.scale_factor_ud -= self.scale_step_ud
                    
                else:
                    self.image = self.orig_image_for_scale.resize((w, h))
                    self.show_image()
                    self.return_image_back = self.orig_image_for_scale
            self.update_undo_redo_buttons()

    def scale_image_down(self):
        if self.orig_image_for_scale or self.orig_image_for_scale_cropped:
            self.undo_stack.append(self.image.copy())
            self.orig_image_for_scale = self.orig_image_for_scale
            self.redo_stack = []
            if 0.98 <= (self.scale_factor_ud - self.scale_step_ud) <= 1.1:
                self.scale_factor_ud -= self.scale_step_ud * 2
            else:
                self.scale_factor_ud -= self.scale_step_ud
            
            
            if self.scale_factor_ud:
                w, h = self.orig_image_for_scale.size
                w = int(w * self.scale_factor_ud)
                h = int(h * self.scale_factor_ud)
                if w >= 200 and h >= 150:
                    
                    self.image = self.orig_image_for_scale.resize((w, h))
                    self.show_image()
                    self.return_image_back = self.orig_image_for_scale
                    

                else:
                    messagebox.showinfo("Внимание", "Минимальный размер достигнут!")
                    self.scale_factor_ud += self.scale_step_ud
                    
            self.update_undo_redo_buttons()
       
    
    

    def save_changes(self):
        if self.image:
            try:
                import os
                if not os.path.exists("photoes"):
                    os.makedirs("photoes")
                self.default_image.save("photoes/original.png")
                if self.image:
                    self.image.save("photoes/edited.png")
                    self.smw.pop()
                messagebox.showinfo("Успех", "Сохранение успешно выполнено!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изменения: {str(e)}")



    def undo_action(self):
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.show_image()
            self.update_undo_redo_buttons()

    def redo_action(self):
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.show_image()
            self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        if self.undo_stack:
            self.undo_button.config(state=tk.NORMAL)
        else:
            self.undo_button.config(state=tk.DISABLED)

        if self.redo_stack:
            self.redo_button.config(state=tk.NORMAL)
        else:
            self.redo_button.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    # image_editor = ImageEditor()

    # tk.Frame()

    frame = tk.Frame(root)
    frame.pack()
    image_editor = ImageEditor(frame)

    root.mainloop()

if __name__ == "__main__":
    main()
