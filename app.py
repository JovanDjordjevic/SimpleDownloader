from PIL import Image, ImageTk
import subprocess
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from availablePrograms import AVAILABLE_PROGRAMS
from utils import *

class SimpleDownloaderApp:
    """
        Main class for Simple Downloader app
    """

    def __init__(self):
        # tkinter widgets and needed tk variables that must be globaly available
        self.mRootElement = tk.Tk()
        self.mDownloadButton = ttk.Button(self.mRootElement, text="Download selected", command=self.onDownloadButtonClicked)
        self.mCurrentStatusVar = tk.StringVar()
        self.mCurrentStatusLabel = ttk.Label(self.mRootElement, textvariable=self.mCurrentStatusVar)
        self.mProgressBarVar = tk.DoubleVar()
        self.mSelectAllVar = tk.BooleanVar()
        self.mLogFrame = VerticallyScrollableFrame(self.mRootElement)
        self.mAllLogsCollapsible = None

        # other needed variables
        self.mAllImages = dict()
        self.mProgramCheckboxes = list()
        self.mNumJobs = 0
        self.mTotalCompletedJobs = 0
        self.mSuccessfulJobs = 0
        self.mFailedJobs = 0

    def refreshEntireUI(self):
        self.mRootElement.update()
        self.mRootElement.update_idletasks()

    def resetVariablesAndUI(self):
        self.mNumJobs = 0
        self.mTotalCompletedJobs = 0
        self.mSuccessfulJobs = 0
        self.mFailedJobs = 0
        self.mCurrentStatusVar.set("")
        self.mProgressBarVar.set(0)

        for widget in self.mLogFrame.interior.winfo_children():
            widget.destroy()

        self.mAllLogsCollapsible = CollapsibleFrame(self.mLogFrame.interior, text='Detailed winget output per program', relief="raised", borderwidth=1)
        self.mAllLogsCollapsible.grid(row=0, column=0, columnspan=len(AVAILABLE_PROGRAMS), sticky="we")

        self.refreshEntireUI()

    def downloadOne(self, programName : str, wingetId : str):
        singleProgramLog = CollapsibleFrame(self.mAllLogsCollapsible.subFrame, text=f"{programName}", relief="raised", borderwidth=1)
        singleProgramLog.grid(pady=2, padx=2, sticky="we")

        wingetOutputTextArea = tk.Text(singleProgramLog.subFrame, wrap=tk.WORD, width=150, height=5)
        wingetOutputTextArea.grid(padx=10, pady=10)

        installedSuccessfully = False

        try:
            wingetOutputTextArea.insert(tk.END, f"Installing {programName}...\n")

            self.mCurrentStatusVar.set(f"{self.mTotalCompletedJobs + 1}/{self.mNumJobs} Installing {programName}...")
            self.refreshEntireUI()

            process = subprocess.Popen(
                ["winget", "install", "-e", "--id", wingetId, "--silent", "--disable-interactivity", 
                "--accept-package-agreements", "--accept-source-agreements"
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            while process.poll() is None:
                output = process.stdout.readline().strip()
                if output:
                    wingetOutputTextArea.insert(tk.END, f"{output}\n")
                    self.refreshEntireUI()

            if process.returncode == 0:
                wingetOutputTextArea.insert(tk.END, f"{programName} has been installed successfully.\n")
                installedSuccessfully = True
            else:
                wingetOutputTextArea.insert(tk.END, f"{programName} was not installed (an error occured or it already exists).\n")

        except Exception as e: 
            wingetOutputTextArea.insert(tk.END, f"Failed to install {programName}. Caught exception: {e}\n")

        indicatorIconPath = ""
        if installedSuccessfully:
            self.mSuccessfulJobs += 1
            indicatorIconPath = "icons/success.ico"
        else:
            self.mFailedJobs += 1
            indicatorIconPath = "icons/error.ico"

        indicatorIcon = ImageTk.PhotoImage(Image.open(indicatorIconPath))
        imageLabel = ttk.Label(singleProgramLog.mainFrame, image=indicatorIcon)
        # Keep a reference to the image to prevent it from being garbage collected
        imageLabel.image = indicatorIcon
        imageLabel.grid(row=0, column=2)

        self.mTotalCompletedJobs += 1
        self.mProgressBarVar.set(self.mTotalCompletedJobs * 100 / self.mNumJobs)
        self.refreshEntireUI()

    def downloadAllSelected(self):
        for programCheckbox in self.mProgramCheckboxes:
            if programCheckbox.isChecked():
                self.downloadOne(programCheckbox.getProgramName(), programCheckbox.getWingetId())

    def onDownloadButtonClicked(self):
        self.resetVariablesAndUI()
        self.mDownloadButton['state'] = tk.DISABLED
        self.refreshEntireUI()

        for programCheckbox in self.mProgramCheckboxes:
            if programCheckbox.isChecked():
                self.mNumJobs += 1

        self.downloadAllSelected()

        self.mDownloadButton['state'] = tk.NORMAL
        self.refreshEntireUI()

    def selectAllPrograms(self):
        for checkbox in self.mProgramCheckboxes:
            checkbox.check()

    def unselectAllPrograms(self):
        for checkbox in self.mProgramCheckboxes:
            checkbox.uncheck()

    def configureStyle(self):
        defaultFont = tkFont.nametofont("TkDefaultFont")
        defaultFont.configure(size=12)

    def setupUI(self):
        self.mRootElement.title("Simple Downloader")

        self.configureStyle()

        mainLabel = ttk.Label(self.mRootElement, text="Select programs you wish to download:")
        mainLabel.grid(row=0, column=0, columnspan=len(AVAILABLE_PROGRAMS))

        optionFrame = ttk.Frame(self.mRootElement)
        optionFrame.grid(row=1, column=0, columnspan=len(AVAILABLE_PROGRAMS))

        selectAllCheckButton = tk.Checkbutton(
            optionFrame, text="Select all", variable=self.mSelectAllVar, onvalue=True, offvalue=False,
            command=lambda: self.selectAllPrograms() if self.mSelectAllVar.get() else self.unselectAllPrograms()
        )
        selectAllCheckButton.grid(row=1, column=0)

        allProgramSectionsFrame = ttk.Frame(self.mRootElement)
        allProgramSectionsFrame.grid(row=2, column=0, columnspan=len(AVAILABLE_PROGRAMS))

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

        self.mDownloadButton.grid(row=3, column=0, columnspan=len(AVAILABLE_PROGRAMS))

        self.mCurrentStatusLabel.grid(row=4, column=0, sticky="we")

        progressBar = ttk.Progressbar(self.mRootElement, orient=tk.HORIZONTAL, variable=self.mProgressBarVar)
        progressBar.grid(row=5, column=0, sticky="we", columnspan=len(AVAILABLE_PROGRAMS), padx=10, pady=10)

        self.mLogFrame.grid(row=6, column=0, sticky="we", columnspan=len(AVAILABLE_PROGRAMS))

    def run(self):
        self.mRootElement.mainloop()
