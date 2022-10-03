""" Microclicker by Colin Vavra """
import json
import csv
from tkinter import DISABLED, NORMAL, Button, Label, Frame, Tk, PhotoImage, Canvas, messagebox
from PIL import Image, ImageTk
from tktooltip import ToolTip

# globals
global_dict = {"money": 0, "full_cps": 0, "cps_overflow": 0}
achievements_dict = {"Habe 100 Chips:": False, "Habe CPS von 50:": False,
                     "Kaufe die Erde:": False, "Kaufe das teuerste Upgrade:": False}
building_buttons, buildings, upgrade_buttons, upgrades = [], [], [], []
save_json = {}

# window
root = Tk()
root.title("MicroClicker")
root.iconbitmap("Emojis/Microchip.ico")
root.geometry("1200x710")
root.resizable(None, None)  # fix window size

# images
bg = PhotoImage(file="Background.png")
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

# extra labels
buildingLb = canvas.create_text(950, 145, text="Gebäude:",
                           font=("helvetica", 18), anchor="nw")
upgradeLb = canvas.create_text(750, 145, text="Upgrades:",
                           font=("helvetica", 18), anchor="nw")


# methods
def read_from_files():
    """ read button data from csv files """
    building_buttons.clear()
    buildings.clear()

    with open("buildings.csv", mode="r", encoding="utf8") as file:
        buildings_csv = csv.reader(file, delimiter=";")
        for i, lines in enumerate(buildings_csv, 0):
            buildings.append(
                Building(root, str(lines[0]), lines[1], lines[2], lines[3]))
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

    check_buttons_enable()
    check_achievements()

    # update main label
    canvas.itemconfig(moneyLb, text=short_number(
        int(global_dict["money"]))+" Chips")

    # recursive call
    root.after(100, loop)


def check_buttons_enable():
    """ check buttons if enable and show """
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


def check_achievements():
    """ checks if achievements are fulfilled """
    if global_dict["money"] >= 100:
        achievements_dict["Habe 100 Chips:"] = True
    if global_dict["full_cps"] >= 50:
        achievements_dict["Habe CPS von 50:"] = True
    if buildings[len(buildings) -1].count >= 1:
        achievements_dict["Kaufe die Erde:"] = True
    if upgrades[len(upgrades) -1].bought:
        achievements_dict["Kaufe das teuerste Upgrade:"] = True


def main_button_pressed():
    """ Microbutton clicked -> money + 1 """
    change_money(1)


def restart_button_pressed():
    """ restart the game -> reset everything """
    global_dict["money"] = 0
    global_dict["full_cps"] = 0
    global_dict["cps_overflow"] = 0
    # reset avievements
    for item in achievements_dict.items():
        achievements_dict[item[0]] = False
    canvas.itemconfig(cpsLb, text=short_number(global_dict["full_cps"]) + " Chips/s")
    read_from_files()


def achievements_button_pressed():
    """ show messagebox about achieved achievements """
    tmp_string = ""
    for item in achievements_dict.items():
        if item[1]:
            tmp_string += item[0] + " --Bekommen--" +"\n"
        else:
            tmp_string += item[0] + " ----" +"\n"
    messagebox.showinfo(title="Achievements", message=tmp_string)


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

    # change globals
    global_dict["money"] = load_json["money"]
    global_dict["full_cps"] = load_json["full_cps"]
    global_dict["cps_overflow"] = load_json["cps_overflow"]
    buildings_json = load_json["buildings"]
    upgrades_json = load_json["upgrades"]

    # clear achievements
    for item in achievements_dict.items():
        achievements_dict[item[0]] = False

    # load buildings
    buildings.clear()
    for i, build_en in enumerate(buildings_json, 0):
        building = Building(root, build_en["name"], int(
            build_en["price"]), int(build_en["cps"]), build_en["tooltip"])
        building.load(build_en)
        buildings.append(building)
        building_buttons.append(canvas.create_window(
            950, i*50+180, anchor="nw", window=buildings[i].get_frame()))
    change_money(0)

    # load upgrades
    upgrades.clear()
    for i, upgrade_en in enumerate(upgrades_json, 0):
        upgrade = Upgrade(root, str(upgrade_en["name"]), upgrade_en["price"],
                          upgrade_en["upgrade"], upgrade_en["tooltip"])
        upgrade.load(upgrade_en)
        upgrades.append(upgrade)
        upgrade_buttons.append(canvas.create_window(
            750, i*40+180, anchor="nw", window=upgrades[i].get_frame()))

    check_buttons_enable()

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


# classes
class ButtonFrame:
    """ Parent class for the button classes """
    def __init__(self, root_window, name, price, tooltip):
        self.name = name
        self.price = price
        self.tooltip = tooltip
        self.state = DISABLED
        self.shown = False
        self.button_img = Image.open("Emojis/" + self.name + ".png")
        self.upgrade_button_resized = ImageTk.PhotoImage(
            self.button_img.resize((20, 20)))
        self.frame = Frame(root_window, borderwidth=0, width=180, height=33)
        self.frame.grid_propagate(False)
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
        ToolTip(self.frame, msg=self.tooltip, follow=True, delay=1.0)

    def disable_button(self):
        """ disable the button """
        self.state = DISABLED
        self.image_button.config(state=self.state)

    def enable_button(self):
        """ enable the button """
        self.state = NORMAL
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
        upgrades_json["tooltip"] = self.tooltip
        upgrades_json["state"] = self.state
        upgrades_json["shown"] = self.shown
        return upgrades_json

    def load(self, attr_json):
        """ load everything from a dict and show if """
        self.name = attr_json["name"]
        self.price = attr_json["price"]
        self.state = attr_json["state"]
        self.shown = attr_json["shown"]
        self.tooltip = attr_json["tooltip"]
        if self.shown:
            self.show_all()
        self.image_button.config(state=self.state)


class Building(ButtonFrame):
    """ Buildings frame, button and counter """
    def __init__(self, root_window, name, price, building_cps, tooltip):
        super().__init__(root_window, name, price, tooltip)
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
        global_dict["full_cps"] += int(self.cps)
        super().upgrade_button_pressed()

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


class Upgrade(ButtonFrame):
    """ Upgrades frame and button """
    def __init__(self, root_window, name, price, upgrade, tooltip):
        super().__init__(root_window, name, price, tooltip)
        self.upgrade = upgrade
        self.bought = False
        self.show_button()

    def show_button(self):
        """ check if to show button and show if """
        if global_dict["money"] >= int(self.price)*0.5:
            self.show_all()
            self.shown = True

    def show_all(self):
        """ place the button and the labels on the grid """
        super().show_all()
        self.price_lb.grid(row=0, column=1, padx=10, pady=5)

    def upgrade_button_pressed(self):
        """ the main button was pressed -> buy upgrade """
        super().upgrade_button_pressed()
        self.upgrade_bought(0)

    def upgrade_bought(self, price):
        """ upgrade the buildings and set as bought"""
        self.disable_button()
        for building in buildings:
            if building.name in self.upgrade:
                building.upgrade_building()
        change_money(-int(price))
        self.bought = True
        self.price_lb.config(text="--Gekauft--")

    def save(self):
        """ save everything in a dict """
        upgrades_json = super().save()
        upgrades_json["upgrade"] = self.upgrade
        upgrades_json["bought"] = self.bought
        return upgrades_json

    def load(self, attr_json):
        """ load everything from a dict and update labels """
        self.upgrade = attr_json["upgrade"]
        self.bought = attr_json["bought"]
        if self.bought:
            self.upgrade_bought(0)


# start the program and read button data
create_buttons()
read_from_files()
loop()
root.mainloop()
