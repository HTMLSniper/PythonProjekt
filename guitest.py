from email.mime import image
from tkinter import *

root = Tk()
root.title("MicroClicker")
root.iconbitmap("Emojis/Microchip.ico")
root.geometry("1200x710")
root.resizable(0,0) # fix window size

# Background
bg = PhotoImage(file="BackgroundGray.png")

# Create Canvas for Background
mainCanvas = Canvas(root, width=1200, height=710)
mainCanvas.pack(fill="both", expand=True)

# Set Background Image for Canvas
mainCanvas.create_image(0,0, image=bg, anchor="nw")

# Add Label to Canvas
mainCanvas.create_text(150,80, text="4000 Chips", font=("helvetica",20), anchor="n")
mainCanvas.create_text(150,110, text="50 Chips/s", font=("helvetica",15), anchor="n")
indexLb = Label(mainCanvas, text = "test")
indexLb.place(x=0,y=0)

# methods

def settings():
  pass

def upgradeButtonPressed():
  pass

def mainButtonPressed():
  pass



# test buttons
""" index = 0
perSec = 0
indexLb = Label(root, text = str(index), width = 20)
perSecLb = Label(root, text = str(perSec), width = 20)
mainButton = Button(root, text = "Press", command = mainButtonPressed, padx=50, pady=50)
upgradeButton = Button(root, text = "+1/s for 20", command = upgradeButtonPressed, state = "disabled")
upgradeButton2 = Button(root, text = "+1/s for 40", command = upgradeButtonPressed, state = "disabled")
upgradeButton3 = Button(root, text = "+1/s for 100", command = upgradeButtonPressed, state = "disabled")
upgradeButton4 = Button(root, text = "+1/s for 200", command = upgradeButtonPressed, state = "disabled")
settingsButton = Button(root, text = "Settings", command = settings)
indexLb.grid(row = 0, column = 0, columnspan = 1, pady = 0)
perSecLb.grid(row = 1, column = 0, columnspan = 1, pady = 0)
mainButton.grid(row = 2, column = 0, rowspan=2,pady = 0)
upgradeButton.grid(row = 0, column = 2, pady = 0)
upgradeButton2.grid(row = 1, column = 2, pady = 0)
upgradeButton3.grid(row = 2, column = 2, pady = 0)
upgradeButton4.grid(row = 3, column = 2, pady = 0)
settingsButton.grid(row = 0, column = 1, pady = 0) """




root.mainloop()