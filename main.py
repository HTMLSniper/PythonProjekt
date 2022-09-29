""" Microclicker by Colin Vavra """
import json
from tkinter import Button, Label, Frame, Tk, PhotoImage, Canvas, messagebox
import csv
from PIL import Image, ImageTk

# globals
global_dict = {"money": 0, "full_cps": 0, "cps_overflow": 0}
building_buttons, buildings, upgrade_buttons, upgrades = [], [], [], []
save_json = {}

# window
root = Tk()
root.title("MicroClicker")
root.iconbitmap("Emojis/Microchip.ico")
root.geometry("1200x710")
root.resizable(0, 0)  # fix window size

# images
bg = PhotoImage(file="Background1.png")
button_img = Image.open("Emojis/Microchip.png")
chip_button_resized = ImageTk.PhotoImage(button_img.resize((300, 300)))

# create canvas for a background picture
canvas = Canvas(root, width=1200, height=710)
canvas.pack(fill="both", expand=True)

# set background image for canvas
canvas.create_image(0, 0, image=bg, anchor="nw")

# add main labels to canvas
moneyLb = canvas.create_text(200, 100, text="0 Chips",
                             font=("helvetica", 25), anchor="n")
cpsLb = canvas.create_text(200, 140, text="0 Chips/s",
                           font=("helvetica", 20), anchor="n")


# methods
def read_from_files():
    """ read button data from csv files """
    building_buttons.clear()
    buildings.clear()

    with open("buildings.csv", mode="r", encoding="utf8") as file:
        buildings_csv = csv.reader(file, delimiter=";")
        for i, lines in enumerate(buildings_csv, 0):
            buildings.append(
                Building(root, str(lines[0]), lines[1], lines[2]))
            building_buttons.append(canvas.create_window(
                950, i*50+180, anchor="nw", window=buildings[i].get_frame()))

    upgrade_buttons.clear()
    upgrades.clear()

    with open("upgrades.csv", mode="r", encoding="utf8") as file:
        upgrades_csv = csv.reader(file, delimiter=";")
        for i, lines in enumerate(upgrades_csv, 0):
            upgrades.append(
                Upgrade(root, str(lines[0]), lines[1], lines[2], lines[3]))
            upgrade_buttons.append(canvas.create_window(
                750, i*40+180, anchor="nw", window=upgrades[i].get_frame()))


def loop():
    """ main loop that handles updates per second """
    # update chips and money
    tmp = global_dict["full_cps"] / 10
    full_tmp = global_dict["full_cps"] // 10
    global_dict["cps_overflow"] += tmp - full_tmp  # handle decimal overflow
    if global_dict["cps_overflow"] >= 1:  # a full chip has been produced
        full_tmp += 1
        global_dict["cps_overflow"] -= 1
    global_dict["money"] += full_tmp  # add cps to money

    # check buttons enable
    for building in buildings:
        if building.shown is False:
            building.show_button()
            break
        if int(building.price) <= global_dict["money"]:
            building.enable_button()
        else:
            building.disable_button()
    for upgrade in upgrades:
        if upgrade.shown is False:
            upgrade.show_button()
            break
        if int(upgrade.price) <= global_dict["money"] and not upgrade.bought:
            upgrade.enable_button()
        else:
            upgrade.disable_button()

    # update main label
    canvas.itemconfig(moneyLb, text=short_number(
        int(global_dict["money"]))+" Chips")

    # recursive call
    root.after(100, loop)


def main_button_pressed():
    """ Microbutton clicked -> money + 1 """
    change_money(1)


def restart_button_pressed():
    """ restart the game -> reset everything """
    global_dict["money"] = 0
    global_dict["full_cps"] = 0
    global_dict["cps_overflow"] = 0
    canvas.itemconfig(cpsLb, text=short_number(global_dict["full_cps"]) + " Chips/s")
    read_from_files()


def achievements_button_pressed():
    """ show messagebox about achieved achievements """
    messagebox.showinfo(title="Achievements", message="None, \n options")


def save_button_pressed():
    """ save everything in a json file """
    save_json["money"] = global_dict["money"]
    save_json["full_cps"] = global_dict["full_cps"]
    save_json["cps_overflow"] = global_dict["cps_overflow"]
    save_json["buildings"] = [x.save() for x in buildings]
    save_json["upgrades"] = [x.save() for x in upgrades]
    with open("mydata.json", "w", encoding="utf-8") as file_save:
        json.dump(save_json, file_save)


def load_button_pressed():
    """ load everything from a json file """
    file_load = open("mydata.json", encoding="utf-8")
    load_json = json.load(file_load)
    global_dict["money"] = load_json["money"]
    global_dict["full_cps"] = load_json["full_cps"]
    global_dict["cps_overflow"] = load_json["cps_overflow"]
    buildings_json = load_json["buildings"]
    upgrades_json = load_json["upgrades"]

    # load buildings
    buildings.clear()
    for i, build_en in enumerate(buildings_json, 0):
        building = Building(root, build_en["name"], int(
            build_en["price"]), int(build_en["cps"]))
        building.load(build_en)
        buildings.append(building)
        building_buttons.append(canvas.create_window(
            950, i*50+180, anchor="nw", window=buildings[i].get_frame()))
    change_money(0)

    # load upgrades
    upgrades.clear()
    for i, upgrade_en in enumerate(upgrades_json, 0):
        upgrade = Upgrade(root, str(upgrade_en["name"]), upgrade_en["price"],
                          upgrade_en["condition"], upgrade_en["upgrade"])
        upgrade.load(upgrade_en)
        upgrades.append(upgrade)
        upgrade_buttons.append(canvas.create_window(
            750, i*40+180, anchor="nw", window=upgrades[i].get_frame()))

    # first check if buttons are visible
    for building in buildings:
        if building.shown is False:
            building.show_button()
            break
        if int(building.price) <= global_dict["money"]:
            building.enable_button()
        else:
            building.disable_button()
    for upgrade in upgrades:
        if upgrade.shown is False:
            upgrade.show_button()
            break
        if int(upgrade.price) <= global_dict["money"] and not upgrade.bought:
            upgrade.enable_button()
        else:
            upgrade.disable_button()

    file_load.close()


def exit_button_pressed():
    """ close the window """
    root.destroy()


def short_number(num):
    """ return a number in a shortened version """
    if 0 <= num < 1000000:
        return str(num)
    if 1000000 <= num < 1000000000:
        return str(round(num/1000000, 3)) + " Millionen"
    if 1000000000 <= num < 1000000000000:
        return str(round(num/1000000000, 3)) + " Milliarden"
    if 1000000000000 <= num < 1000000000000000:
        return str(round(num/1000000000000, 3)) + " Billionen"
    if 1000000000000000 <= num <= 1000000000000000000:
        return str(round(num/1000000000000000, 3)) + " Billiarden"
    # else to big
    return num


def change_money(diff):
    """ change money by diff """
    global_dict["money"] += diff
    canvas.itemconfig(moneyLb, text=short_number(global_dict["money"]) + " Chips")
    canvas.itemconfig(cpsLb, text=short_number(global_dict["full_cps"]) + " Chips/s")


def create_buttons():
    """ create and place main buttons """
    chip_button = Button(root, image=chip_button_resized,
                         command=main_button_pressed, borderwidth=2, width=300, height=300)
    restart_button = Button(root, text="Neustart",
                            command=restart_button_pressed, width=20)
    achievements_button = Button(root, text="Achievements",
                                 command=achievements_button_pressed, width=20)
    save_button = Button(root, text="Speichern",
                         command=save_button_pressed, width=20)
    load_button = Button(root, text="Laden",
                         command=load_button_pressed, width=20)
    exit_button = Button(root, text="Verlassen",
                         command=exit_button_pressed, width=20)
    canvas.create_window(50, 250, anchor="nw", window=chip_button)
    canvas.create_window(600, 100, anchor="n", window=restart_button)
    canvas.create_window(600, 150, anchor="n", window=achievements_button)
    canvas.create_window(600, 200, anchor="n", window=save_button)
    canvas.create_window(600, 250, anchor="n", window=load_button)
    canvas.create_window(600, 600, anchor="n", window=exit_button)

class ButtonFrame:
    """ Parent class for the button classes """
    def __init__(self, root_window, name, price):
        self.name = name
        self.price = price
        self.state = "disabled"
        self.shown = False
        self.button_img = Image.open("Emojis/" + self.name + ".png")
        self.upgrade_button_resized = ImageTk.PhotoImage(
            self.button_img.resize((20, 20)))
        self.frame = Frame(root_window, borderwidth=0, width=180, height=33)
        self.frame.grid_propagate(0)
        self.price_lb = Label(self.frame, text=str(
            self.price) + " Chips", font=("helvetica", 10))
        self.image_button = Button(self.frame, image=self.upgrade_button_resized,
                                   command=self.upgrade_button_pressed, borderwidth=0,
                                   width=33, height=33, state=self.state)
        self.frame.grid_columnconfigure(1, weight=1)

    def get_frame(self):
        """ returns the frame """
        return self.frame

    def show_all(self):
        """ place the button on the grid """
        self.image_button.grid(row=0, column=0, rowspan=2, pady=0, sticky="w")

    def disable_button(self):
        """ disable the button """
        self.state = "disabled"
        self.image_button.config(state=self.state)

    def enable_button(self):
        """ enable the button """
        self.state = "normal"
        self.image_button.config(state=self.state)

    def upgrade_button_pressed(self):
        """ the main button was pressed"""
        self.disable_button()
        change_money(-int(self.price))

    def save(self):
        """ saves everything of class in a dict """
        upgrades_json = {}
        upgrades_json["name"] = self.name
        upgrades_json["price"] = self.price
        upgrades_json["state"] = self.state
        upgrades_json["shown"] = self.shown
        return upgrades_json

    def load(self, attr_json):
        """ load everything from a dict and show if """
        self.name = attr_json["name"]
        self.price = attr_json["price"]
        self.state = attr_json["state"]
        self.shown = attr_json["shown"]
        if self.shown:
            self.show_all()
        self.image_button.config(state=self.state)


class Building(ButtonFrame):
    """ Buildings frame, button and counter """
    def __init__(self, root_window, name, price, building_cps):
        super().__init__(root_window, name, price)
        self.start_price = price
        self.cps = building_cps
        self.count = 0
        self.building_button_resized = ImageTk.PhotoImage(
            self.button_img.resize((30, 30)))
        self.frame.config(height=48)
        self.frame.pack(fill="x")
        self.image_button.config(width=40, height=40)
        self.cps_lb = Label(self.frame, text=str(self.cps) +
                            " Chips/s", font=("helvetica", 10))
        self.count_lb = Label(self.frame, text=str(
            self.count), font=("helvetica", 20), fg="gray")
        self.show_button()

    def show_button(self):
        """ check if to show button and show if """
        if global_dict["money"] >= int(self.start_price)*0.5:
            self.show_all()
            self.shown = True

    def show_all(self):
        """ place the button and the labels on the grid """
        super().show_all()
        self.price_lb.grid(row=0, column=1, padx=10, sticky="n")
        self.cps_lb.grid(row=1, column=1, padx=10, sticky="s")
        self.count_lb.grid(row=0, column=2, rowspan=2,
                           pady=5, padx=5, sticky="e")

    def upgrade_button_pressed(self):
        """ the main button was pressed -> buy building """
        super().upgrade_button_pressed()
        global_dict["full_cps"] += int(self.cps)

        self.count += 1
        # calculate new price for next building
        self.price = int(int(self.start_price) * pow(1.15, int(self.count)))

        self.count_lb.config(text=str(self.count))
        self.price_lb.config(text=str(self.price)+" Chips")

    def upgrade_building(self):
        """ upgrade for this building was bought """
        global_dict["full_cps"] += int(self.cps)*int(self.count)
        # double the cps
        self.cps = int(self.cps) * 2
        self.cps_lb.config(text=str(self.cps)+" Chips/s")

    def save(self):
        """ save everything in a dict """
        buildings_json = super().save()
        buildings_json["start_price"] = self.start_price
        buildings_json["cps"] = self.cps
        buildings_json["count"] = self.count
        return buildings_json

    def load(self, attr_json):
        """ load everything from a dict and update labels """
        super().load(attr_json)
        self.start_price = attr_json["start_price"]
        self.cps = attr_json["cps"]
        self.count = attr_json["count"]
        self.count_lb.config(text=str(self.count))
        self.price_lb.config(text=str(self.price)+" Chips")
        self.cps_lb.config(text=str(self.cps)+" Chips/s")

# TODO Aufräumen + Kommentare

class Upgrade:
    """ Upgrades frame and button """
    def __init__(self, root_window, name, price, condition, upgrade):
        self.name = name
        self.price = price
        self.condition = condition
        self.upgrade = upgrade
        self.state = "disabled"
        self.bought = False
        self.shown = False
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
        self.show_button()
        self.frame.grid_columnconfigure(1, weight=1)

    def show_button(self):
        """_summary_
        """
        if global_dict["money"] >= int(self.price)*0.5:
            self.show_all()
            self.shown = True

    def show_all(self):
        """_summary_
        """
        self.image_button.grid(row=0, column=0, rowspan=2, pady=0, sticky="w")
        self.price_lb.grid(row=0, column=1, padx=10, pady=5)

    def get_frame(self):
        """_summary_

        Returns:
            Frame: Frame of Building
        """
        return self.frame

    def upgrade_button_pressed(self):
        """_summary_
        """
        self.bought = True
        self.upgrade_bought(self.price)

    def upgrade_bought(self, price):
        """_summary_
        """
        self.disable_button()
        for building in buildings:
            if building.name in self.upgrade:
                building.upgrade_building()
        change_money(-int(price))
        self.price_lb.config(text="--Gekauft--")

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

    def save(self):
        """_summary_
        """
        upgrades_json = {}
        upgrades_json["name"] = self.name
        upgrades_json["price"] = self.price
        upgrades_json["condition"] = self.condition
        upgrades_json["upgrade"] = self.upgrade
        upgrades_json["state"] = self.state
        upgrades_json["bought"] = self.bought
        upgrades_json["shown"] = self.shown
        return upgrades_json

    def load(self, upgrades_json):
        """_summary_
        """
        self.name = upgrades_json["name"]
        self.price = int(upgrades_json["price"])
        self.condition = upgrades_json["condition"]
        self.upgrade = upgrades_json["upgrade"]
        self.bought = upgrades_json["bought"]
        self.state = upgrades_json["state"]
        self.shown = upgrades_json["shown"]
        if self.shown:
            self.show_all()
        if self.bought:
            self.upgrade_bought(0)
        self.image_button.config(state=self.state)


# start the program and read button data
read_from_files()
loop()
root.mainloop()
