import tkinter as tk
from ttkbootstrap import ttk

class ScrollableFrame:
    """
        A frame with both vertical and horizontal scrolling.
        If you only need one specific direction of scrolling, 
        the other one can be disabled during construction
    """
    def __init__(self, root, allowHorizontalScroll=True, allowVerticalScroll=True, *args, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)

        self.outerFrame = tk.Frame(root, *args, **kwargs)
        self.outerFrame.rowconfigure(0, weight=1)
        self.outerFrame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.outerFrame, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        
        if allowHorizontalScroll:
            self.horizontalScrollbar = ttk.Scrollbar(self.outerFrame, orient=tk.HORIZONTAL)
            self.horizontalScrollbar.grid(row=1, column=0, sticky='ew')
            self.canvas['xscrollcommand'] = self.horizontalScrollbar.set
            self.horizontalScrollbar['command'] = self.canvas.xview

        if allowVerticalScroll:
            self.verticalScrollbar = ttk.Scrollbar(self.outerFrame, orient=tk.VERTICAL)
            self.verticalScrollbar.grid(row=0, column=1, sticky='ns')
            self.canvas['yscrollcommand'] = self.verticalScrollbar.set
            self.verticalScrollbar['command'] = self.canvas.yview

        self.innerFrame = tk.Frame(self.canvas)

        self.canvas.create_window(0, 0, window=self.innerFrame, anchor='nw')
        self.innerFrame.bind("<Configure>", self.on_frame_configure)

        self.outerFrameAttributes = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outerFrameAttributes:
            return getattr(self.outerFrame, item)
        else:
            return getattr(self.innerFrame, item)

    def on_frame_configure(self, event=None):
        _, _, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion = (0,0, max(x2, width), max(y2, height)))

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
