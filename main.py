import tkinter as tk
from tkinter import CENTER, ttk
import time


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(self)
        self.title("MicroClicker")
        self.geometry("700x500")
        self.index = 0
        self.perSec = 0
        self.indexLb = ttk.Label(self, text = str(self.index), width = 20)
        self.perSecLb = ttk.Label(self, text = str(self.perSec), width = 20)
        self.mainButton = ttk.Button(self, text = "Press", command = self.mainButtonPressed)
        
        self.upgradeButton = ttk.Button(self, text = "+1/s for 20", command = self.upgradeButtonPressed, state = "disabled")
        self.upgradeButton2 = ttk.Button(self, text = "+1/s for 40", command = self.upgradeButtonPressed, state = "disabled")
        self.upgradeButton3 = ttk.Button(self, text = "+1/s for 100", command = self.upgradeButtonPressed, state = "disabled")
        self.upgradeButton4 = ttk.Button(self, text = "+1/s for 200", command = self.upgradeButtonPressed, state = "disabled")
        
        self.settingsButton = ttk.Button(self, text = "Settings", command = self.settings)
        
        
        self.indexLb.grid(row = 0, column = 0, columnspan = 1, pady = 0)
        self.perSecLb.grid(row = 1, column = 0, columnspan = 1, pady = 0)
        self.mainButton.grid(row = 2, column = 0, rowspan=2,pady = 0)
        self.upgradeButton.grid(row = 0, column = 2, pady = 0)
        self.upgradeButton2.grid(row = 1, column = 2, pady = 0)
        self.upgradeButton3.grid(row = 2, column = 2, pady = 0)
        self.upgradeButton4.grid(row = 3, column = 2, pady = 0)
        self.settingsButton.grid(row = 0, column = 1, pady = 0)
        
        self.updateNumbers()
        self.mainloop()
        
    def mainButtonPressed(self):
        self.index += 1
        self.indexLb.config(text = str(self.index))
        
    def upgradeButtonPressed(self):
        self.perSec += 1
        self.perSecLb.config(text = str(self.perSec))
        self.upgradeButton.config(text = "+1/s for 30")
        
    def checkCanBuy(self):
        if self.index >= 20:
            self.upgradeButton.config(state = "normal")
        
        
    def updateNumbers(self):
        self.index += self.perSec
        self.indexLb.config(text = str(self.index))
        self.perSecLb.config(text = str(self.perSec))
        self.checkCanBuy()
        self.after(1000,lambda: self.updateNumbers())
        
    def settings(self):
        pass

""" class UpgradeButton():
    def __init__(self, root, text):
        self.root = root
        self.index = 0
        self.perSec = perSec
        self.cost = cost
        
        self.text = createText()
        self.command = self.pressed
        self.state = "disabled"
        self.button = ttk.Button(self.root, text = self.text, command = self.command, state = self.state)
    
    def createText(self):
        text = str(self.perSec) + " für " + str(self.cost)
        return text
    
    def updateButton(self):
        self.button.config(self.root, text = self.text, state = self.state)
    
    def checkDisabled(self, index):
        if index >= self.cost:
            self.state = "normal"
            updateButton()
    
    def upgradeIndex(self):
        pass
    
    def pressed(self):
        self.root.upgradeBought(self.cost)
        self.index =+ 1
        self.state = "disabled" """
        
            

if __name__ == "__main__":
    gui = Gui()

