import tkinter as tk
from tkinter import ttk

class ProgramCheckbox:
    """
        Class that wraps a program to it's associated checkbox
    """

    def __init__(self, programName : str, wingetId : str, root) -> None:
        self.programName = programName
        self.wingetId = wingetId

        self.checkBoxVar = tk.BooleanVar()
        checkbox = ttk.Checkbutton(root, text=self.programName, variable=self.checkBoxVar)
        checkbox.grid(row=0, column=1)

    def isChecked(self) -> bool:
        return self.checkBoxVar.get() == True
    
    def check(self) -> None:
        self.checkBoxVar.set(True)

    def uncheck(self) -> None:
        self.checkBoxVar.set(False)

    def toggle(self) -> None:
        self.checkBoxVar.set(not self.checkBoxVar.get())

    def getProgramName(self) -> str:
        return self.programName

    def getWingetId(self) -> str:
        return self.wingetId

class CollapsibleFrame(tk.Frame):
    """
        A collapsible frame that can hold other widgets inside of it
    """

    def __init__(self, parent, text="", *args, **kwargs) -> None:
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

    def toggle(self) -> None:
        if self.show.get():
            self.subFrame.grid()
            self.toggleButton.configure(text='-')
        else:
            self.subFrame.grid_forget()
            self.toggleButton.configure(text='+')

class VerticallyScrollableFrame(ttk.Frame):
    """
        A frame that can be scrolled vertically
    """

    def __init__(self, parent, *args, **kwargs) -> None:
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=tk.FALSE, padx=20)

        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.TRUE)

        vscrollbar.config(command=self.canvas.yview)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(self.canvas)
        self.interiorId = self.canvas.create_window(0, 0, window=interior,  anchor=tk.NW)

        self.interior.bind('<Configure>', self.configureInterior)
        self.canvas.bind('<Configure>', self.configureCanvas)

    def configureInterior(self, event) -> None:
        # Update the scrollbars to match the size of the inner frame.
        interiorWidth = self.interior.winfo_reqwidth()

        self.canvas.config(scrollregion=f"0 0 {interiorWidth} {self.interior.winfo_reqheight()}")

        if interiorWidth != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width=interiorWidth)

    def configureCanvas(self, event) -> None:
        canvasWidth = self.canvas.winfo_width()

        if self.interior.winfo_reqwidth() != canvasWidth:
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interiorId, width=canvasWidth)
