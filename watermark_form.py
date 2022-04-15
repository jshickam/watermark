from tkinter import Button, Entry, Frame, Label, ttk, Image, StringVar, filedialog as fd, messagebox
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os

class ImageBox(Label):
    def __init__(self, parent, watermark):
        """Creates a new image box containing a blank image.
        Provide the parent tkinter object as parent.
        provide the watermark object as watermark."""

        super().__init__(parent)
        self.watermark = watermark
        self.image = Image.new(size=(640, 480), mode="RGBA", color="gray")
        self.photo = ImageTk.PhotoImage(self.image)
        self.configure(image=self.photo, padx=5, pady=5)

    def update_watermark(self):
        """Combines the watermark text with the image"""
        image = self.image.resize((640, int(640 * (self.image.height / self.image.width))), Image.ANTIALIAS)
        
        # create the transparent watermark
        txt = Image.new('RGBA', image.size) 
        d = ImageDraw.Draw(txt, "RGBA")
        font = ImageFont.FreeTypeFont("fonts/Yacimiento ExtraBold Ex.ttf", size=self.watermark.font_size)
        if self.watermark.text != "":
            txt = txt.resize(d.textsize(self.watermark.text, font))
        d = ImageDraw.Draw(txt, "RGBA")
        
        d.text(xy=(0, 0),
                text=self.watermark.text, 
                fill=(self.watermark.color),  
                font=font)
        starting_width = txt.width
        starting_height = txt.height

        # rotate the watermark 
        txt = txt.rotate(self.watermark.rotation, expand=True)

        # relocate the watermark after rotation
        offset_x = int((txt.width - starting_width) / 2)
        offset_y = int((txt.height - starting_height) / 2)
        image.paste(txt, (self.watermark.x - offset_x, self.watermark.y - offset_y), txt)
        self.photo = ImageTk.PhotoImage(image)
        self.composite_image = image
        self.configure(image=self.photo)

    def update_photo(self, path):
        """Loads the file at the given path into the ImageBox"""
        try:
            self.image = Image.open(path).convert("RGBA")
        except PIL.UnidentifiedImageError:
            messagebox.showerror("Invalid image", f"{path} is not a valid image file.")

    def save(self):
        """Combines the watermark text with the full-size image and saves file"""
        image = self.image.copy()

        # ratio of the displayed image to the full size image
        resize_ratio = image.width / 640

        # create the transparent watermark
        txt = Image.new('RGBA', image.size) 
        d = ImageDraw.Draw(txt, "RGBA")
        resized_font = int(self.watermark.font_size * resize_ratio)
        font = ImageFont.FreeTypeFont("fonts/Yacimiento ExtraBold Ex.ttf", size=resized_font)
        if self.watermark.text != "":
            txt = txt.resize(d.textsize(self.watermark.text, font))
        d = ImageDraw.Draw(txt, "RGBA")
        
        d.text(xy=(0, 0),
                text=self.watermark.text, 
                fill=(self.watermark.color),  
                font=font)

        # rotate the watermark 
        starting_width = txt.width
        starting_height = txt.height
        txt = txt.rotate(self.watermark.rotation, expand=True)

        # relocate the watermark after rotation
        offset_x = int((txt.width - starting_width) / 2)
        offset_y = int((txt.height - starting_height) / 2)

        x_loc = int(self.watermark.x * resize_ratio - offset_x)
        y_loc = int(self.watermark.y * resize_ratio - offset_y)
        image.paste(txt, (x_loc, y_loc), txt)

        #file_path = fd.asksaveasfile(mode='w', defaultextension=".png")
        
        file_path = fd.asksaveasfilename(confirmoverwrite=True, 
                                         defaultextension="png", 
                                         filetypes=[("jpeg", ".jpg"),
                                                    ("png", ".png"), 
                                                    ("bitmap", "bmp"),
                                                    ("gif", ".gif") ])
        if file_path is not None: # if dialog not closed with "cancel".
            # Convert to RGB if saving as jpeg
            if os.path.splitext(file_path)[1] == ".jpg":
                image = image.convert("RGB")
            image.save(fp=file_path)
            

class ColorWidget(Frame):
    def __init__(self, frame, callback):
        """Creates a ColorWidget object containing multiple color selections
        Provide the parent tkinter object and a callback function that handles the button clicks"""
        
        super().__init__(frame)
        self.selected_color = "white"
        style = ttk.Style()
        
        label = ttk.Label(self, text="Color")
        label.grid(column=0, row=0, columnspan=3)
        # Configure button styles and create color buttons
        colors_list = ["White", "Black", "Blue", "Yellow", "Green", "Red", "Purple", "Orange", "Brown"]
        style = ttk.Style()

        # Create the color buttons and associate the callback to the command
        for num, color in enumerate(colors_list):
            style.configure(f"{color}.TButton", foreground=color.lower(), width=1)
            btn = ttk.Button(self, 
                            style=f"{color}.TButton", 
                            text="█",
                            command=lambda color=color: callback(color.lower()))
            # Rows of 3
            btn.grid(row=int(num / 3) + 1, column=num % 3)


# Placement button widget
class DirectionWidget(Frame):
    def __init__(self, frame, callback):
        """Creates a DirectionWidget that moves the watermark in any direction
        provide the parent tkinter object and a callback to handle the button clicks"""

        super().__init__(frame)
        buttons = [{"text": "▲", "direction": "up", "col": 1, "row": 0},
                   {"text": "◀", "direction": "left", "col": 0, "row": 1},
                   {"text": "▶", "direction": "right", "col": 2, "row": 1},
                   {"text": "▼", "direction": "down", "col": 1, "row": 2}] 
        
        # Create buttons  
        for button in buttons:
            btn = ttk.Button(self, 
                             text=button["text"], 
                             width=1, 
                             command=lambda direction=button["direction"]: callback(direction))
            btn.grid(column=button["col"], row=button["row"])

class RotationWidget(Frame):
    def __init__(self, frame, callback):
        """Creates a RotationWidget object that rotates the watermark clockwise or counter-clockwise
        provide the parent tkinter object and a callback that handles the button clicks"""

        super().__init__(frame)
        Label(self, text="Rotate").grid(column=0, row=0, columnspan=2)
        clockwise_button = ttk.Button(self, 
                           text="↻", 
                           width=1, 
                           command=lambda: callback("right"))
        clockwise_button.grid(column=0, row=1)
        counter_clockwise_button = ttk.Button(self, 
                           text="↺", 
                           width=1, 
                           command=lambda: callback("left"))
        counter_clockwise_button.grid(column=1, row=1)

class OpacityWidget(Frame):     
    def __init__(self, frame, callback):
        """Creates an OpacityWidget object that raises or lowers the opacity of the watermark.
        Provide the parent tkinter object and a callback that handles the button clicks"""

        super().__init__(frame)
        Label(self, text="Opacity:").grid(column=0, row=0, columnspan=2)
        up_button = ttk.Button(self, 
                           text="▲", 
                           width=1, 
                           command=lambda: callback("up"))
        up_button.grid(column=0, row=1)
        down_button = ttk.Button(self, 
                           text="▼", 
                           width=1, 
                           command=lambda: callback("down"))
        down_button.grid(column=1, row=1)

class TextEntryWidget(Frame):
    def __init__(self, parent, callback):
        """Creates a TextEntryWidget object with a textbox that sets the watermark text.
        Provide the parent tkinter object and a callback called when the text changes"""
        super().__init__(parent)
        Label(self, text="Text:").grid(column=0, row=0)
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
        self.text_entry = Entry(self, textvariable=sv, width=66)
        self.text_entry.grid(column=1, row=0)


class SizeWidget(Frame):
    def __init__(self, parent, callback):
        """Creates a SizeWidget object that allows changing the watermark font size.
        Provide the parent tkinter object and a callback that handles the selection changing of the drop-down"""
        super().__init__(parent)
        ttk.Label(self, text="Font Size:").grid(column=0, row=0)
        self.size_dropdown = ttk.Combobox(self, 
                                          values=[i for i in range(10, 200, 4)],
                                          state="readonly",
                                          width=3
                                          )
        self.size_dropdown.current(10)
        self.size_dropdown.bind('<<ComboboxSelected>>', callback)
        self.size_dropdown.grid(column=1, row=0)
    
    def get_value(self):
        """Returns the font size selected in the dropdown"""
        return self.size_dropdown.get()

# Open and save buttons
class OpenSaveWidget(Frame):
    def __init__(self, parent, open_callback, save_callback):
        """Creates a new Open and Save button widget
        Provide both an open_callback function and a save_callback function to handle button clicks"""

        super().__init__(parent)
        self.open_button = Button(self, text="📂", command=open_callback)
        self.open_button.grid(column=0, row=0)
        self.save_button = Button(self, text="💾", command=save_callback, state="disabled")
        self.save_button.grid(column=1, row=0)
    
    def enable_save(self):
        self.save_button.configure(state="normal")
        
# Watermark object and methods.
# Supply the main Tk Toplevel widget
class Watermark():
    def __init__(self, parent):
        """Creates a new Watermark object.  Provide the parent ImageBox object"""
        self.parent = parent
        self.font_size = 50
        self.opacity = 25
        self.color = (255, 255, 255, self.opacity)
        self.rotation = 0
        self.x = 50
        self.y = 50
        self.text = ""

    def move(self, direction):
        """Changes the x and y cordinates of the Watermark object by 10 pixels
        direction needs to be a string containing 'up', 'down', 'left', or 'right'"""
        if direction == "up":
                self.y -= 10
        elif direction == "down":
                self.y += 10
        elif direction == "left":
                self.x -= 10
        elif direction == "right":
                self.x += 10
        #self.parent.update_text()
    
    def change_color(self, color=None):
        """Changes color of the watermark.
           color is a named color string
        """
        if color == None:
            list_color = list(self.color)[:3]
        else:
            list_color = list(self.parent.winfo_rgb(color))
        
        list_color.append(self.opacity)
        self.color = tuple(list_color)

    def change_size(self, event, size):
        """Changes the font_size of the watermark"""
        self.font_size = int(size)
        

    def change_opacity(self, direction):
        """Changes the opacity of the watermark
        direction is a string, either "up" or "down".  "up" makes it more opaque, "down" makes it more transparent"""
        if direction == "up":
            if self.opacity < 255:
                self.opacity += 5
        else:
            if self.opacity > 0:
                self.opacity -= 5
        self.change_color()

    def rotate(self, direction):
        """Rotates the watermark clockwise or counter-clockwise
        direction should be "left" for counter-clockwise or "right" for clockwise"""
        if direction == "left":
            if self.rotation == 355:
                self.rotation = 0
            else:
                self.rotation += 5
        else:
            if self.rotation == 0:
                self.rotation = 355
            else:
                self.rotation -= 5