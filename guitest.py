from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("MicroClicker")
root.iconbitmap("Emojis/Microchip.ico")
root.geometry("1200x710")
root.resizable(0,0) # fix window size

# Background
bg = PhotoImage(file="BackgroundGray.png")
buttonImg = Image.open("Emojis/Auto.png")
buttonResized= ImageTk.PhotoImage(buttonImg.resize((20,20)))

# Create Canvas for Background
mainCanvas = Canvas(root, width=1200, height=710)
mainCanvas.pack(fill="both", expand=True)

# Set Background Image for Canvas
mainCanvas.create_image(0,0, image=bg, anchor="nw")

# methods

def settings():
  pass

def upgradeButtonPressed():
  pass

def mainButtonPressed():
  pass


# Add Label to Canvas
mainCanvas.create_text(150,80, text="4000 Chips", font=("helvetica",20), anchor="n")
test = mainCanvas.create_text(150,110, text="50 Chips/s", font=("helvetica",15), anchor="n")
upgradeButton = Button(root, text = "+1/s for 20", command = upgradeButtonPressed, state = "disabled")
buyAuto = Button(root, image=buttonResized, command=upgradeButtonPressed, borderwidth=0, width=20, height=20, state="disabled")
test2 = mainCanvas.create_window(1000, 80, anchor="nw", window=upgradeButton)
test3 = mainCanvas.create_window(1000, 120, anchor="n", window=buyAuto)
mainCanvas.itemconfig(test ,text="100 Chips/s")


class Building:
  def __init__(self, root, image, price, cps):
    self.price = price
    self.cps = cps
    self.count = 0
    self.state = "normal"
    self.buttonImg = Image.open(image)
    self.buttonResized = ImageTk.PhotoImage(self.buttonImg.resize((20,20)))
    self.frame = Frame(root, borderwidth = 0, width = 100, height = 40)
    self.imageButton = Button(self.frame, image = self.buttonResized, command = self.upgradeButtonPressed, borderwidth = 0, width = 20, height = 20, state = self.state)
    self.priceLb = Label(self.frame, text = str(self.price) + " Chips")
    self.cpsLb = Label(self.frame, text = str(self.cps) + " Chips/s")
    self.imageButton.pack(side="left", padx=10)
    self.priceLb.pack(padx=10)
    self.cpsLb.pack(padx=10)
  
  def getFrame(self):
    return self.frame
  
  def upgradeButtonPressed(self):
    self.disableButton()
  
  def disableButton(self):
    self.state = "disabled"
    self.imageButton.config(state=self.state)

hand = Building(root, "Emojis/Hand.png", 10, 1)
handWindow = mainCanvas.create_window(1000, 200, anchor="n", window=hand.getFrame())
mechaniker = Building(root, "Emojis/Mechaniker.png", 50, 3)
mechanikerWindow = mainCanvas.create_window(1000, 250, anchor="n", window=mechaniker.getFrame())
zelt = Building(root, "Emojis/Zelt.png", 100, 5)
zeltWindow = mainCanvas.create_window(1000, 300, anchor="n", window=zelt.getFrame())
haus = Building(root, "Emojis/Haus.png", 200, 10)
hausWindow = mainCanvas.create_window(1000, 350, anchor="n", window=haus.getFrame())
fabrik = Building(root, "Emojis/Fabrik.png", 1000, 25)
fabrikWindow = mainCanvas.create_window(1000, 400, anchor="n", window=fabrik.getFrame())
stadion = Building(root, "Emojis/Stadion.png", 2000, 50)
stadiomWindow = mainCanvas.create_window(1000, 450, anchor="n", window=stadion.getFrame())

"""
class filterswindow:
    '''
    Interface graphique recapitulant les caracteristique du sismogramme
    presentant les options de filtrage et de calculs du noyau de sensibilite
    '''
    def __init__(self,racine):
        self.canvas = Canvas(racine, borderwidth=1, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(racine, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        self.data()
            
    def data(self):
        global filterVar
        filterVar = 1
        global text6a
        text6a = "1"
        global text6c1
        text6c1 = StringVar()
        global text6c2
        text6c2 = StringVar()
        global text6c3
        text6c3 = StringVar()
           
        Label(self.frame, text="Option Filter").grid(row=0)
        Label(self.frame, text="\n").grid(row=1)
        
        Label(self.frame, text="lowest frequency ?").grid(row=4)
        e1 = Entry(self.frame, textvariable=text6c1)
        e1.grid(row=5)
        
        Label(self.frame, text="highest frequency ?").grid(row=20)
        e2 = Entry(self.frame, textvariable=text6c2)
        e2.grid(row=21)
        
        Label(self.frame, text="number of poles ?").grid(row=22)
        e3 = Entry(self.frame, textvariable=text6c3)
        e3.grid(row=23)
                    
        Button(self.frame, text="continue", command=self.quitter).grid(row=24)
                  
    def quitter(self):
        global racine
        racine.destroy()
        afficheSismoFiltre(textPath.get(), float(text6c1.get()), float(text6c2.get()), float(text6c3.get()))
            
    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

testframe = filterswindow(root)
  """

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