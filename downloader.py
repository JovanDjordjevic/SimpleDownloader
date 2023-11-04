import tkinter as tk
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk

# list of programs that are available for installation.
# Key is "section name" and value is a map where key is "program name" and value is "winget id"
PROGRAM_LIST = {
    "Dev editors" : {
        "VS Code" : "Microsoft.VisualStudioCode",
        "Visual Studio Community 2022" : "Microsoft.VisualStudio.2022.Community",
        "PyCharm Community Edition"  : "JetBrains.PyCharm.Community",
        "IntelliJ IDEA Community Edition" : "JetBrains.IntelliJIDEA.Community",
        "Atom" : "GitHub.Atom",
        "Android Studio" : "Google.AndroidStudio",
        "Notepad++" : "Notepad++.Notepad++",
    },
    "Dev tools" : {
        "Postman" : "Postman.Postman",
        "Windows Terminal" : "Microsoft.WindowsTerminal",
        "Git" : "Git.Git",
        "Node.js" : "OpenJS.NodeJS",
        "Python 3.12" : "Python.Python.3.12",
        "Python 2.7" : "Python.Python.2",
        "Java 8" : "Oracle.JavaRuntimeEnvironment",
        "PuTTY" : "PuTTY.PuTTY",
    },
    "Communication" : {
        "Discord" : "Discord.Discord",
        "Zoom" : "Zoom.Zoom",
        "Microsoft Teams" : "Microsoft.Teams",
        "Cisco webex" : "Cisco.WebexTeams",
        "Telegram Desktop" : "Telegram.TelegramDesktop",
        "Skype" : "Microsoft.Skype",
    },
    "Game launchers" : {
        "Steam" : "Valve.Steam",
        "Epic Games Launcher" : "EpicGames.EpicGamesLauncher",
        "EA app" : "ElectronicArts.EADesktop",
    },
    "Media" : {
        "VLC media player" : "VideoLAN.VLC",
        "Spotify" : "Spotify.Spotify",
        "OBS Studio" : "OBSProject.OBSStudio",
    },
    "Browsers" : {
        "Google Chrome" : "Google.Chrome",
        "Opera GX" : "Opera.OperaGX",
        "Mozilla Firefox" : "Mozilla.Firefox",
    },
    "Other" : {
        "MSI Afterburner" : "Guru3D.Afterburner",
        "Rivatuner Statistics Server" : "Guru3D.RTSS",
        "HWiNFO" : "REALiX.HWiNFO",
        "QTTabBar" : "QTTabBar.QTTabBar",
        "qBittorrent" : "qBittorrent.qBittorrent",
        "SignalRgb" : "WhirlwindFX.SignalRgb",
        "Display Driver Uninstaller" : "Wagnardsoft.DisplayDriverUninstaller",
        "WinRAR" : "RARLab.WinRAR",
        "7-Zip" : "7zip.7zip",
        "VMware Workstation Player" : "VMware.WorkstationPlayer",
        "NZXT CAM" : "NZXT.CAM",
        "CinebenchR23" : "Maxon.CinebenchR23",
        "Heaven Benchmark" : "Unigine.HeavenBenchmark",
    },
}

CHECKBOXES = []

class ProgramCheckbox:
    def __init__(self, programName : str, wingetId : str, root):
        self.programName = programName
        self.wingetId = wingetId

        self.checkBoxVar = tk.BooleanVar()
        checkbox = ttk.Checkbutton(root, text=self.programName, variable=self.checkBoxVar)
        checkbox.pack(side=tk.LEFT)

    def isChecked(self):
        return self.checkBoxVar.get() == True
    
    def getProgramName(self):
        return self.programName

    def getWingetId(self):
        return self.wingetId

def downloadOne(programName : str, wingetId : str):
    try:
        print(f"Installing {programName}...")
        process = subprocess.Popen(["winget", "install", "-e", "--id", wingetId], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            if output:
                print(output.strip())

        if process.returncode == 0:
            print(f"{programName} has been installed successfully.")
        else:
            print(f"{programName} was not installed (an error occured or it already exists).")
    except Exception as e: 
        print(f"Failed to install {programName}. Caught exception: {e}")

def downloadAllSelected():
    for programCheckbox in CHECKBOXES:
        if programCheckbox.isChecked():
            downloadOne(programCheckbox.getProgramName(), programCheckbox.getWingetId())

def main():
    root = tk.Tk()
    root.title("Simple downloader")

    label = ttk.Label(root, text="Select programs you wish to download:")
    label.pack(side=tk.TOP)

    checkboxSectionsFrame = ttk.Frame(root)
    checkboxSectionsFrame.pack(padx=10, pady=10)

    for sectionName, progToWingetIdMap in PROGRAM_LIST.items():
        singleSectionFrame = ttk.Frame(checkboxSectionsFrame)
        singleSectionFrame.pack(side=tk.LEFT, padx=20)

        ttk.Label(singleSectionFrame, text=sectionName).pack(side=tk.TOP)
        ttk.Label(singleSectionFrame, text="").pack(side=tk.TOP) # empty label for spacing

        for programName, wingetId in progToWingetIdMap.items():
            checkboxAndIconFrame = ttk.Frame(singleSectionFrame)
            checkboxAndIconFrame.pack(side=tk.TOP)
            CHECKBOXES.append(ProgramCheckbox(programName, wingetId, checkboxAndIconFrame))

            image = Image.open(f"icons/{wingetId}.png").resize((30, 30))

            icon = ImageTk.PhotoImage(image)
            imageLabel = ttk.Label(checkboxAndIconFrame, image=icon)
            imageLabel.image = icon  # Keep a reference to the image to prevent it from being garbage collected
            imageLabel.pack(side=tk.RIGHT, padx=5)

    downloadButton = ttk.Button(root, text="Download selected", command=downloadAllSelected)
    downloadButton.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
