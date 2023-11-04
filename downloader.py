import tkinter as tk
import subprocess

PROGRAM_NAME_TO_WINGET_ID = {
    #dev
    "VS Code" : "Microsoft.VisualStudioCode",
    "Postman" : "Postman.Postman",
    "Windows Terminal" : "Microsoft.WindowsTerminal",

    # communication
    "Discord" : "Discord.Discord",

    # game launchers
    "Steam" : "Valve.Steam",

    # browsers
    "Google Chrome" : "Google.Chrome",
    "Opera GX" : "Opera.OperaGX",

    # other
    "MSI Afterburner" : "Guru3D.Afterburner",
    "Rivatuner Statistics Server" : "Guru3D.RTSS",
    "QTTabBar" : "QTTabBar.QTTabBar",
}

CHECKBOXES = []

class ProgramCheckbox:
    def __init__(self, programName : str, wingetId : str, root):
        self.programName = programName
        self.wingetId = wingetId

        self.checkBoxVar = tk.IntVar()
        checkbox = tk.Checkbutton(root, text=self.programName, variable=self.checkBoxVar)
        checkbox.pack()

    def isChecked(self):
        return self.checkBoxVar.get() == 1
    
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

    label = tk.Label(root, text="Select programs you wish to download:")
    label.pack()

    # Create checkbox for each program
    for program, wingetId in PROGRAM_NAME_TO_WINGET_ID.items():
        CHECKBOXES.append(ProgramCheckbox(program, wingetId, root))

    downloadButton = tk.Button(root, text="Download selected", command=downloadAllSelected)
    downloadButton.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
