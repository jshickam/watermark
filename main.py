from tkinter import ttk, Tk, filedialog as fd
from tkinter import filedialog
from tkinter import messagebox
from watermark_form import *
from PIL import ImageTk, Image

def select_file():
        """Handles the Open button click event. Prompts user to select a file and loads it into
        photo_label.
        """
        filename = fd.askopenfilename(filetypes=[("jpeg", ".jpg .jpeg"),
                                                 ("png", ".png"), 
                                                 ("bitmap", "bmp"),
                                                 ("gif", ".gif") ])
        if filename != "":
            photo_box.update_photo(filename) 
            photo_box.update_watermark()

            # resize window to fit resized photo (640 width)
            window.geometry(f"810x{int(640 * (photo_box.image.height / photo_box.image.width) + 45)}")
            open_save.enable_save()


# Set up window
window = Tk()
window.geometry("810x525")
window.title("Watermark")
window.resizable(False, False)


def on_color_change(color):
    watermark.change_color(color)
    photo_box.update_watermark()

def on_size_change(event):
    watermark.change_size(event, size_widget.get_value())
    photo_box.update_watermark()

def on_text_change(sv):
    watermark.text = sv.get()
    photo_box.update_watermark()

def on_rotate(direction):
    watermark.rotate(direction)
    photo_box.update_watermark()

def on_move(direction):
    watermark.move(direction)
    photo_box.update_watermark()

def on_opacity_change(direction):
    watermark.change_opacity(direction)
    photo_box.update_watermark()

watermark = Watermark(window)
watermark.text = ""

# Image box
photo_box = ImageBox(window, watermark)
photo_box.grid(column=0, row=0, rowspan=5, padx=5)

watermark_text = TextEntryWidget(window, on_text_change)
watermark_text.grid(column=0, row=5, padx=6, pady=5)

color_control = ColorWidget(window, on_color_change)
color_control.grid(column=1, row=0)
# Watermark size control
size_widget = SizeWidget(window, on_size_change)
size_widget.grid(column=1, row=1)
OpacityWidget(window, on_opacity_change).grid(column=1, row=2)
DirectionWidget(window, on_move).grid(column=1, row=3)
RotationWidget(window, on_rotate).grid(column=1, row=4)
open_save = OpenSaveWidget(window, select_file, photo_box.save)
open_save.grid(column=1, row=5)
window.mainloop()

