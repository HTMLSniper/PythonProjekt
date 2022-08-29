"""_summary_

    Returns:
    _type_: _description_
"""
from ast import Lambda
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

money = 0
full_cps = 0
cps_overflow = 0

# methods


def settings():
    """_summary_
    """


def main_button_pressed():
    """_summary_
    """
    change_money(1)
    
def change_money(diff):
    global money, canvas, cpsLb
    money += diff
    canvas.itemconfig(moneyLb, text=str(money)+" Chips")
    canvas.itemconfig(cpsLb, text=str(full_cps)+" Chips/s")


# Add Label to Canvas
moneyLb = canvas.create_text(200, 100, text="0 Chips",
                             font=("helvetica", 25), anchor="n")
cpsLb = canvas.create_text(
    200, 140, text="10 Chips/s", font=("helvetica", 20), anchor="n")
chip_button = Button(root, image=chip_button_resized,
                     command=main_button_pressed, borderwidth=2, width=300, height=300)
canvas.create_window(50, 250, anchor="nw", window=chip_button)

canvas.itemconfig(cpsLb, text="0 Chips/s")


class Building:
    """_summary_
    """

    def __init__(self, root_window, name, price, building_cps):
        self.name = name
        self.start_price = price
        self.price = price
        self.cps = building_cps
        self.count = 0
        self.state = "disabled"
        self.building_opened_img = Image.open("Emojis/"+name+".png")
        self.building_button_resized = ImageTk.PhotoImage(
            self.building_opened_img.resize((30, 30)))
        self.frame = Frame(root_window, borderwidth=0, width=180, height=48)
        self.frame.grid_propagate(0)
        self.frame.pack(fill="x")
        self.image_button = Button(self.frame, image=self.building_button_resized,
                                   command=self.upgrade_button_pressed, borderwidth=0,
                                   width=40, height=40, state=self.state)
        self.price_lb = Label(self.frame, text=str(
            self.price) + " Chips", font=("helvetica", 10))
        self.cps_lb = Label(self.frame, text=str(self.cps) +
                            " Chips/s", font=("helvetica", 10))
        self.count_lb = Label(self.frame, text=str(
            self.count), font=("helvetica", 20), fg="gray")
        self.image_button.grid(row=0, column=0, rowspan=2, pady=0, sticky="w")
        self.price_lb.grid(row=0, column=1, padx=10, sticky="n")
        self.cps_lb.grid(row=1, column=1, padx=10, sticky="s")
        self.count_lb.grid(row=0, column=2, rowspan=2,
                           pady=5, padx=5, sticky="e")
        self.frame.grid_columnconfigure(1, weight=1)

    def get_frame(self):
        """_summary_

        Returns:
            Frame: Frame of Building
        """
        return self.frame

    def upgrade_button_pressed(self):
        """_summary_
        """
        global full_cps
        full_cps += int(self.cps)
        change_money(-int(self.price))
    
        self.count += 1
        self.price = int(self.count) * 5 + int(self.start_price)
        
        self.count_lb.config(text=str(self.count))
        self.price_lb.config(text=str(self.price)+" Chips")
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
    
    def upgrade_building(self):
        """_summary_
        """
        global full_cps
        full_cps += int(self.cps)*int(self.count)
        self.cps *= 2
        self.cps_lb.config(text=str(self.cps)+" Chips/s")


class Upgrade:
    """_summary_
    """

    def __init__(self, root_window, name, price, condition, upgrade):
        self.name = name
        self.price = price
        self.condition = condition
        self.upgrade = upgrade
        self.state = "disabled"
        self.bought = False
        self.upgrade_opened_img = Image.open("Emojis/"+name+".png")
        self.upgrade_button_resized = ImageTk.PhotoImage(
            self.upgrade_opened_img.resize((20, 20)))

        self.frame = Frame(root_window, borderwidth=0, width=180, height=33)
        self.frame.grid_propagate(0)
        self.image_button = Button(self.frame, image=self.upgrade_button_resized,
                                   command=self.upgrade_button_pressed, borderwidth=0,
                                   width=33, height=33, state=self.state)
        self.price_lb = Label(self.frame, text=str(
            self.price) + " Chips", font=("helvetica", 10))
        self.image_button.grid(row=0, column=0, rowspan=2, pady=0, sticky="w")
        self.price_lb.grid(row=0, column=1, padx=10, pady=5)
        self.frame.grid_columnconfigure(1, weight=1)

    def get_frame(self):
        """_summary_

        Returns:
            Frame: Frame of Building
        """
        return self.frame

    def upgrade_button_pressed(self):
        """_summary_
        """
        global full_cps, buildings
        for building in buildings:
            if building.name in self.upgrade:
                building.upgrade_building()
        change_money(-int(self.price))
        self.bought = True
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
            Building(root, str(lines[0]), lines[1], lines[2]))
        building_buttons.append(canvas.create_window(
            950, i*50+180, anchor="nw", window=buildings[i].get_frame()))


upgrade_buttons = []
upgrades = []

with open("upgrades.csv", mode="r", encoding="utf8") as file:
    upgrades_csv = csv.reader(file, delimiter=";")
    for i, lines in enumerate(upgrades_csv, 0):
        upgrades.append(
            Upgrade(root, str(lines[0]), lines[1], lines[2], lines[3]))
        upgrade_buttons.append(canvas.create_window(
            750, i*40+180, anchor="nw", window=upgrades[i].get_frame()))


def loop():
    """_summary_
    """
    # update Chips
    global money, full_cps, cps_overflow, moneyLb, buildings
    tmp = full_cps / 10
    full_tmp = full_cps // 10
    cps_overflow += tmp - full_tmp # handle decimal overflow
    if cps_overflow >=10: # a full chip has been produced
        full_tmp += 1
        cps_overflow -= 10
    money += full_tmp # add cps to money
    
    # check buttons enable
    for building in buildings:
        if (int(building.price) <= money):
            building.enable_button()
        else:
            building.disable_button()
    for upgrade in upgrades:
        if (int(upgrade.price) <= money and not upgrade.bought):
            upgrade.enable_button()
        else:
            upgrade.disable_button()
    canvas.itemconfig(moneyLb, text=str(int(money))+" Chips") # update Label
    root.after(100, loop)

loop()
root.mainloop()
