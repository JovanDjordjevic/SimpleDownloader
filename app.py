from PIL import Image, ImageTk
import subprocess
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from enum import Enum
from availablePrograms import AVAILABLE_PROGRAMS
from customWidgets import ScrollableFrame, ProgramCheckbox, CollapsibleFrame

class operationType(str, Enum):
    INSTALL = "install",
    UNINSTALL = "uninstall"

class SimpleDownloaderApp:
    """
        Main class for Simple Downloader app
    """

    def __init__(self) -> None:
        # tkinter widgets and needed tk variables that must be globaly available
        self.mRootElement = tk.Tk()
        self.mRootFrame = ScrollableFrame(self.mRootElement)
        self.mButtonFrame = ttk.Frame(self.mRootFrame)
        self.mInstallButton = ttk.Button(self.mButtonFrame, text="Install selected", command=self.onInstallButtonClicked)
        self.mUninstallButton = ttk.Button(self.mButtonFrame, text="Uninstall selected", command=self.onUninstallButtonClicked)
        self.mCurrentStatusVar = tk.StringVar()
        self.mCurrentStatusLabel = ttk.Label(self.mRootFrame, textvariable=self.mCurrentStatusVar)
        self.mProgressBarVar = tk.DoubleVar()
        self.mSelectAllVar = tk.BooleanVar(value=False)
        self.mRequireUserInputVar = tk.BooleanVar(value=False)
        self.mLogFrame = ScrollableFrame(self.mRootFrame, allowHorizontalScroll=False)
        self.mAllLogsCollapsible = None

        # other needed variables
        self.mAllImages = dict()
        self.mProgramCheckboxes = list()
        self.mNumJobs = 0
        self.mTotalCompletedJobs = 0
        self.mSuccessfulJobs = 0
        self.mFailedJobs = 0

        self.setupUI()

    def refreshEntireUI(self) -> None:
        self.mRootElement.update()
        self.mRootElement.update_idletasks()

    def resetVariablesAndUI(self) -> None:
        self.mNumJobs = 0
        self.mTotalCompletedJobs = 0
        self.mSuccessfulJobs = 0
        self.mFailedJobs = 0
        self.mCurrentStatusVar.set("")
        self.mProgressBarVar.set(0)

        for widget in self.mLogFrame.innerFrame.winfo_children():
            widget.destroy()

        self.mAllLogsCollapsible = CollapsibleFrame(self.mLogFrame, text='Detailed winget output per program', relief="raised", borderwidth=1)
        self.mAllLogsCollapsible.grid(row=0, column=0, columnspan=len(AVAILABLE_PROGRAMS), sticky="we")

        self.refreshEntireUI()

    def handleSingleProgram(self, programName : str, wingetId : str, operation : operationType) -> None:
        singleProgramLog = CollapsibleFrame(self.mAllLogsCollapsible.subFrame, text=f"{programName}", relief="raised", borderwidth=1)
        singleProgramLog.grid(pady=2, padx=2, sticky="we")

        wingetOutputTextArea = tk.Text(singleProgramLog.subFrame, wrap=tk.WORD, width=150, height=5)
        wingetOutputTextArea.grid(padx=10, pady=10)

        handledSuccessfully = False

        try:
            wingetOutputTextArea.insert(tk.END, f"Installing {programName}...\n")

            self.mCurrentStatusVar.set(f"{self.mTotalCompletedJobs + 1}/{self.mNumJobs} Installing {programName}...")
            self.refreshEntireUI()
            
            operationCmd = "install" if operation == operationType.INSTALL else "uninstall"

            wingetOptions = ["winget", operationCmd, "-e", "--id", wingetId]

            if operation == operationType.INSTALL:
                wingetOptions.append("--accept-package-agreements")
                wingetOptions.append("--accept-source-agreements")

            if self.mRequireUserInputVar.get() == False:
                wingetOptions.append("--silent")
                wingetOptions.append("--disable-interactivity")

            wingetOutputTextArea.insert(tk.END, f"Running winget with command:\n\t{' '.join(wingetOptions)}\n")

            process = subprocess.Popen(wingetOptions, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            while process.poll() is None:
                output = process.stdout.readline().strip()
                if output and len(output) > 1:
                    wingetOutputTextArea.insert(tk.END, f"{output}\n")
                    self.refreshEntireUI()

            if process.returncode == 0:
                wingetOutputTextArea.insert(tk.END, f"{programName} has been {operationCmd}ed successfully.\n")
                handledSuccessfully = True
            else:
                additionalInfo = "already exists" if operation == operationType.INSTALL else "does not exist"
                wingetOutputTextArea.insert(tk.END, f"{programName} was not {operationCmd}ed (an error occured or it {additionalInfo}).\n")

        except Exception as e: 
            wingetOutputTextArea.insert(tk.END, f"Failed to {operationCmd} {programName}. Caught exception: {e}\n")

        indicatorIconPath = ""
        if handledSuccessfully:
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

    def installAllSelected(self) -> None:
        for programCheckbox in self.mProgramCheckboxes:
            if programCheckbox.isChecked():
                self.handleSingleProgram(programCheckbox.getProgramName(), programCheckbox.getWingetId(), operationType.INSTALL)

    def uninstallAllSelected(self) -> None:
        for programCheckbox in self.mProgramCheckboxes:
            if programCheckbox.isChecked():
                self.handleSingleProgram(programCheckbox.getProgramName(), programCheckbox.getWingetId(), operationType.UNINSTALL)

    def onInstallButtonClicked(self) -> None:
        self.resetVariablesAndUI()
        self.mInstallButton['state'] = tk.DISABLED
        self.refreshEntireUI()

        for programCheckbox in self.mProgramCheckboxes:
            if programCheckbox.isChecked():
                self.mNumJobs += 1

        self.installAllSelected()

        self.mInstallButton['state'] = tk.NORMAL
        self.refreshEntireUI()

    def onUninstallButtonClicked(self) -> None:
        self.resetVariablesAndUI()
        self.mUninstallButton['state'] = tk.DISABLED
        self.refreshEntireUI()

        for programCheckbox in self.mProgramCheckboxes:
            if programCheckbox.isChecked():
                self.mNumJobs += 1

        self.uninstallAllSelected()

        self.mUninstallButton['state'] = tk.NORMAL
        self.refreshEntireUI()

    def selectAllPrograms(self) -> None:
        for checkbox in self.mProgramCheckboxes:
            checkbox.check()

    def unselectAllPrograms(self) -> None:
        for checkbox in self.mProgramCheckboxes:
            checkbox.uncheck()

    def configureStyle(self) -> None:
        defaultFont = tkFont.nametofont("TkDefaultFont")
        defaultFont.configure(size=12)

    def setupOptionsFrame(self) -> None:
        optionFrame = ttk.Frame(self.mRootFrame)
        optionFrame.grid(row=1, column=0, columnspan=len(AVAILABLE_PROGRAMS))

        selectAllCheckbutton = tk.Checkbutton(
            optionFrame, text="Select all", variable=self.mSelectAllVar, onvalue=True, offvalue=False,
            command=lambda: self.selectAllPrograms() if self.mSelectAllVar.get() else self.unselectAllPrograms()
        )
        selectAllCheckbutton.grid(row=1, column=0)

        requireUserInputCheckutton = tk.Checkbutton(
            optionFrame, text="Require user input during installation/uninstallation", 
            variable=self.mRequireUserInputVar, onvalue=True, offvalue=False
        )
        requireUserInputCheckutton.grid(row=1, column=1)

    def setupButtonFrame(self) -> None:
        self.mButtonFrame.grid(row=3, column=0, columnspan=len(AVAILABLE_PROGRAMS))
        self.mInstallButton.grid(row=0, column=0)
        self.mUninstallButton.grid(row=0, column=1)

    def setupProgramSelectionFrame(self) -> None:
        allProgramSectionsFrame = ttk.Frame(self.mRootFrame)
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

    def setupUI(self) -> None:
        self.configureStyle()

        self.mRootElement.title("Simple Downloader")
        self.mRootElement.geometry("1600x900")

        self.mRootFrame.pack(fill=tk.BOTH, expand=True)

        mainLabel = ttk.Label(self.mRootFrame, text="Select programs you wish to download:")
        mainLabel.grid(row=0, column=0, columnspan=len(AVAILABLE_PROGRAMS))

        self.setupOptionsFrame()

        self.setupProgramSelectionFrame()

        self.setupButtonFrame()

        self.mCurrentStatusLabel.grid(row=4, column=0, sticky="we")

        progressBar = ttk.Progressbar(self.mRootFrame, orient=tk.HORIZONTAL, variable=self.mProgressBarVar)
        progressBar.grid(row=5, column=0, sticky="we", columnspan=len(AVAILABLE_PROGRAMS), padx=10, pady=10)

        self.mLogFrame.grid(row=6, column=0, sticky="we", columnspan=len(AVAILABLE_PROGRAMS))

    def run(self) -> None:
        self.mRootElement.mainloop()
