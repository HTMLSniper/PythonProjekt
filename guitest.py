"""_summary_

    Returns:
    _type_: _description_
"""
from tkinter import Button, Label, Frame, Tk, PhotoImage, Canvas
import csv
from PIL import Image, ImageTk


root = Tk()
root.title("MicroClicker")
root.iconbitmap("Emojis/Microchip.ico")
root.geometry("1200x710")
root.resizable(0, 0)  # fix window size

# Background
bg = PhotoImage(file="BackgroundGray.png")
button_img = Image.open("Emojis/Microchip.png")
chip_button_resized = ImageTk.PhotoImage(button_img.resize((300, 300)))

# Create Canvas for Background
canvas = Canvas(root, width=1200, height=710)
canvas.pack(fill="both", expand=True)

# Set Background Image for Canvas
canvas.create_image(0, 0, image=bg, anchor="nw")

# methods


def settings():
    """_summary_
    """


def upgrade_button_pressed():
    """_summary_
    """


def main_button_pressed():
    """_summary_
    """


# Add Label to Canvas
money = canvas.create_text(200, 100, text="4000 Chips",
                           font=("helvetica", 25), anchor="n")
cps = canvas.create_text(
    200, 140, text="50 Chips/s", font=("helvetica", 20), anchor="n")
chip_button = Button(root, image=chip_button_resized,
                     command=main_button_pressed, borderwidth=2, width=300, height=300)
canvas.create_window(50, 250, anchor="nw", window=chip_button)

canvas.itemconfig(cps, text="100 Chips/s")


class Building:
    """_summary_
    """

    def __init__(self, root_window, image, price, building_cps):
        self.name = image
        self.price = price
        self.cps = building_cps
        self.count = 0
        self.state = "disabled"
        self.button_img = Image.open(image)
        self.button_resized = ImageTk.PhotoImage(
            self.button_img.resize((30, 30)))
        self.frame = Frame(root_window, borderwidth=0, width=180, height=48)
        self.frame.grid_propagate(0)
        self.image_button = Button(self.frame, image=self.button_resized,
                                   command=self.upgrade_button_pressed, borderwidth=0,
                                   width=40, height=40, state=self.state)
        self.price_lb = Label(self.frame, text=str(
            self.price) + " Chips", font=("helvetica", 10))
        self.cps_lb = Label(self.frame, text=str(self.cps) +
                            " Chips/s", font=("helvetica", 10))
        self.count_lb = Label(self.frame, text=str(
            self.count), font=("helvetica", 20))
        self.image_button.grid(row=0, column=0, rowspan=2, pady=0)
        self.price_lb.grid(row=0, column=1, padx=10)
        self.cps_lb.grid(row=1, column=1,  padx=10)
        self.count_lb.grid(row=0, column=2, rowspan=2, pady=5, padx=5)

    def get_frame(self):
        """_summary_

        Returns:
            Frame: Frame of Building
        """
        return self.frame

    def upgrade_button_pressed(self):
        """_summary_
        """
        self.disable_button()

    def disable_button(self):
        """_summary_
        """
        self.state = "disabled"
        self.image_button.config(state=self.state)

    def enable_button(self):
        """_summary_
        """
        self.state = "normal"
        self.image_button.config(state=self.state)


building_buttons = []
buildings = []

with open("buildings.csv", mode="r", encoding="utf8") as file:
    buildings_csv = csv.reader(file, delimiter=";")
    for i, lines in enumerate(buildings_csv, 0):
        buildings.append(
            Building(root, "Emojis/"+str(lines[0])+".png", lines[1], lines[2]))
        building_buttons.append(canvas.create_window(
            950, i*50+180, anchor="nw", window=buildings[i].get_frame()))


root.mainloop()
