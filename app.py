from PIL import Image, ImageTk
import subprocess
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from availablePrograms import AVAILABLE_PROGRAMS

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

class SimpleDownloaderApp:
    """
        Main class for Simple Downloader app
    """

    def __init__(self):
        # tkinter widgets and needed tk variables that must be globaly available
        self.mRootElement = tk.Tk()
        self.mDownloadButton = ttk.Button(self.mRootElement, text="Download selected", command=self.onDownloadButtonClicked)
        self.mProgressBarVar = tk.DoubleVar()
        # other needed variables
        self.mAllImages = dict()
        self.mProgramCheckboxes = list()
        self.mNumJobs = 0
        self.mTotalCompletedJobs = 0
        self.mSuccessfulJobs = 0
        self.mFailedJobs = 0

    def resetVariablesAndUI(self):
        self.mNumJobs = 0
        self.mTotalCompletedJobs = 0
        self.mSuccessfulJobs = 0
        self.mFailedJobs = 0
        self.mProgressBarVar.set(0)

    def downloadOne(self, programName : str, wingetId : str):
        try:
            print(f"Installing {programName}...")
            process = subprocess.Popen(["winget", "install", "-e", "--id", wingetId], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            while process.poll() is None:
                output = process.stdout.readline()
                if output:
                    print(output.strip())

            if process.returncode == 0:
                print(f"{programName} has been installed successfully.")
                self.mSuccessfulJobs += 1
            else:
                print(f"{programName} was not installed (an error occured or it already exists).")
                self.mFailedJobs += 1

        except Exception as e: 
            print(f"Failed to install {programName}. Caught exception: {e}")
            self.mFailedJobs += 1

        self.mTotalCompletedJobs += 1
        self.mProgressBarVar.set(self.mTotalCompletedJobs * 100 / self.mNumJobs)
        self.mRootElement.update_idletasks()

    def downloadAllSelected(self):
        for programCheckbox in self.mProgramCheckboxes:
            if programCheckbox.isChecked():
                self.downloadOne(programCheckbox.getProgramName(), programCheckbox.getWingetId())

    def onDownloadButtonClicked(self):
        self.resetVariablesAndUI()
        self.mDownloadButton['state'] = tk.DISABLED
        self.mRootElement.update_idletasks()

        for programCheckbox in self.mProgramCheckboxes:
            if programCheckbox.isChecked():
                self.mNumJobs += 1

        self.downloadAllSelected()

        self.mDownloadButton['state'] = tk.NORMAL
        self.mRootElement.update_idletasks()

    def configureStyle(self):
        defaultFont = tkFont.nametofont("TkDefaultFont")
        defaultFont.configure(size=12)

    def setupUI(self):
        self.mRootElement.title("Simple Downloader")

        self.configureStyle()

        mainLabel = ttk.Label(self.mRootElement, text="Select programs you wish to download:")
        mainLabel.grid(row=0, column=0, columnspan=len(AVAILABLE_PROGRAMS))
        
        allProgramSectionsFrame = ttk.Frame(self.mRootElement)
        allProgramSectionsFrame.grid(row=1, column=0, columnspan=len(AVAILABLE_PROGRAMS))

        currentSectionColumn = 0
        for sectionName, progToWingetIdMap in AVAILABLE_PROGRAMS.items():
            singleSectionFrame = ttk.LabelFrame(allProgramSectionsFrame)
            singleSectionFrame.grid(row=0, column=currentSectionColumn, sticky="ns", padx=5, pady=10)

            sectionLabel = ttk.Label(singleSectionFrame, text=sectionName)
            sectionLabel.grid(row=0, column=0)

            singleProgramRow = 1
            for programName, wingetId in progToWingetIdMap.items():
                checkboxAndIconFrame = ttk.Frame(singleSectionFrame)
                checkboxAndIconFrame.grid(row=singleProgramRow, column=0, sticky="we")

                # Keep a reference to the image to prevent it from being garbage collected
                self.mAllImages[programName] = ImageTk.PhotoImage(
                    Image.open(f"icons/{wingetId}.ico")
                )

                # image will be container within a label isntead of text
                imageLabel = ttk.Label(checkboxAndIconFrame, image=self.mAllImages[programName])
                imageLabel.grid(row=0, column=0)

                # checkboxes will have (row=0, column=1)
                self.mProgramCheckboxes.append(ProgramCheckbox(programName, wingetId, checkboxAndIconFrame))

                singleProgramRow += 1
            
            currentSectionColumn += 1

        self.mDownloadButton.grid(row=2, column=0, columnspan=len(AVAILABLE_PROGRAMS))

        progressBar = ttk.Progressbar(self.mRootElement, orient=tk.HORIZONTAL, variable=self.mProgressBarVar)
        progressBar.grid(row=3, column=0, sticky="we", columnspan=len(AVAILABLE_PROGRAMS), padx=10, pady=10)

    def run(self):
        self.mRootElement.mainloop()
