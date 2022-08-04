import tkinter as tk
from tkinter import ttk
import time


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(self)
        self.index = 0
        self.perSec = 0
        self.indexLb = ttk.Label(self, text = str(self.index), width = 20)
        self.perSecLb = ttk.Label(self, text = str(self.perSec), width = 20)
        self.mainButton = ttk.Button(self, text = "Press", command = self.mainButtonPressed)
        self.upgradeButton = ttk.Button(self, text = "+1/s for 20", command = self.upgradeButtonPressed, state = "disabled")
        
        
        self.indexLb.grid(row = 0, column = 0, columnspan = 1, pady = 5)
        self.perSecLb.grid(row = 1, column = 0, columnspan = 1, pady = 5)
        self.mainButton.grid(row = 2, column = 0, pady = 5)
        self.upgradeButton.grid(row = 0, column = 1, pady = 5)
        
        self.updateNumbers()
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

if __name__ == "__main__":
    app = App()
    app.mainloop()

# from tkinter import *
# 
# class Gui(Tk):
#     def __init__(self):
#         super.__init__()
#         self.index = 0
#         self.perSec = 0
#         self.root = Tk()
#         self.indexLb = Label(self.root, text = str(self.index), width = 20)
#         self.perSecLb = Label(self.root, text = str(self.perSec), width = 20)
#         self.mainButton = Button(self.root, text = "Press", command = self.mainButtonPressed)
#         self.upgradeButton = Button(self.root, text = "+1/s", command = self.upgradeButtonPressed)
#         
#         
#         self.indexLb.grid(row = 0, column = 0, columnspan = 1, pady = 5)
#         self.perSecLb.grid(row = 1, column = 0, columnspan = 1, pady = 5)
#         self.mainButton.grid(row = 2, column = 0, pady = 5)
#         self.upgradeButton.grid(row = 0, column = 1, pady = 5)
#         
#         self.updateNumbers()
#         self.root.mainloop()
#     
#     def mainButtonPressed(self):
#         self.index += 1
#         self.indexLb.config(text = str(self.index))
#         
#     def upgradeButtonPressed(self):
#         self.perSec += 1
#         self.perSecLb.config(text = str(self.perSec))
#         
#         
#     def updateNumbers(self):
#         self.index += self.perSec
#         self.indexLb.config(text = str(self.index))
#         self.perSecLb.config(text = str(self.perSec))
#         self.after(1000, self.updateNumbers)
#         
#         
# test = Gui()