import tkinter as tk
from tkinter import ttk

class ProgramCheckbox:
    """
        Class that wraps a program to it's associated checkbox
    """

    def __init__(self, programName : str, wingetId : str, root):
        self.programName = programName
        self.wingetId = wingetId

        self.checkBoxVar = tk.BooleanVar()
        checkbox = ttk.Checkbutton(root, text=self.programName, variable=self.checkBoxVar)
        checkbox.grid(row=0, column=1)

    def isChecked(self):
        return self.checkBoxVar.get() == True
    
    def getProgramName(self):
        return self.programName

    def getWingetId(self):
        return self.wingetId

class CollapsibleFrame(tk.Frame):
    """
        A collapsible frame that can hold other widgets inside of it
    """

    def __init__(self, parent, text="", *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.show = tk.BooleanVar()
        self.show.set(False)

        self.mainFrame = ttk.Frame(self)
        self.mainFrame.grid(row=0, column=0, sticky="we")

        self.toggleButton = ttk.Checkbutton(self.mainFrame, width=3, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggleButton.grid(row=0, column=0)

        ttk.Label(self.mainFrame, text=text).grid(row=0, column=1)

        # insert all sub elements into this subFrame
        self.subFrame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if self.show.get():
            self.subFrame.grid()
            self.toggleButton.configure(text='-')
        else:
            self.subFrame.grid_forget()
            self.toggleButton.configure(text='+')
