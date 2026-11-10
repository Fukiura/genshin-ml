from tkinter import *
from tkinter import ttk
from time import sleep
import json
import subprocess
import os
import adminperms

#adminperms.request_admin_privileges()

# Debugging
def printInfo(inputs: list[Entry]) -> None:
    for i in inputs:
        print(i.get())


class EntryModified(Entry):
    previousText: str = ""

    def insert(self, index, string):
        self.previousText = self.get()
        super().insert(index=index, string=string)

class Status:
    """
        The status for the program, remains primarily as a static class
    """
    mgt_inst: subprocess.Popen | None = None
    fpsUnlk_inst: subprocess.Popen | None = None
    genshin_inst: str | None = None
    runningProcessesList: list[str] | None = None
    is_running: bool = False
    delay_genshin_detection: int = 5
    changedFileLocation: bool = False

    @staticmethod
    def detect_genshin_process() -> bool:
        cmd: subprocess.CompletedProcess = subprocess.run(["tasklist"], capture_output=True)
        runningProcessesList = cmd.stdout.decode().split("\n")

        for i in runningProcessesList:
            if "Genshin" in i:
                Status.genshin_inst = i
                return True
        
        return False

    @staticmethod
    def genshin_running_while_loop() -> None:
        while Status.detect_genshin_process():
            sleep(Status.delay_genshin_detection)
        Status.is_running = False


def consolePrint(*msgs: object, startString: str = "", endString: str = "", commaModifier:str = " ") -> None:
    r""" 
        Customized print, used for the console interface and python's terminal

        startString appends before the output

        endString appends after the output
        
        commaModifier changes the way the set of msgs joined together:
            consolePrint("banana", "apple", commaModifier = "\n"); output: "banana\napple"
    """
    stringMsg = startString + commaModifier.join(map(str, msgs)) + endString
    print(stringMsg)

def runButton_handler(mgt: EntryModified, fpsUnlkr: EntryModified) -> None:
    """ Function for button handler, specifically runButton """
    if (not Status.is_running and 
        os.path.exists(mgt.get()) and mgt.get().endswith(".exe") and
        os.path.exists(fpsUnlkr.get()) and fpsUnlkr.get().endswith(".exe")):
        Status.is_running = True
        Status.mgt_inst = subprocess.Popen([mgt.get()])
        Status.fpsUnlk_inst = subprocess.Popen([fpsUnlkr.get()])

    save_file_location(mgt, fpsUnlkr)

def save_file_location(mgt: EntryModified, fpsUnlkr: EntryModified) -> None:
    """
        Writes the inputted file locations from in1 and in2(EntryModified objects).
        It doesn't write if either objects aren't changed(their text content)
    """
    if mgt.previousText != mgt.get() or fpsUnlkr.previousText != fpsUnlkr.get():
        x = json.dumps({
            "3DMigoto File Location": mgt.get(),
            "Fps Unlocker File Location": fpsUnlkr.get()
        }, indent=4)
        with open("settings.json", "w") as f:
            f.write(x)

def initialize_save_file_location(mgt: EntryModified, fpsUnlkr: EntryModified) -> None:
    """ If the file exists, initialize the saved file, a file called "settings.json" """
    x: dict[str, str] = {}
    with open("settings.json", "r") as f:
        x = json.loads(f.read())

    if os.path.exists(os.path.join(os.getcwd(), "settings.json")):
        if x.get("3DMigoto File Location") != None:
            mgt.insert(0, x.get("3DMigoto File Location", ""))
        if x.get("Fps Unlocker File Location") != None:
            fpsUnlkr.insert(0, x.get("Fps Unlocker File Location", ""))

def exit_handler() -> None:
    consolePrint("Closing")
    
    if Status.mgt_inst:
        if Status.mgt_inst.poll() is None:
            Status.mgt_inst.terminate()
        Status.mgt_inst = None

    if Status.fpsUnlk_inst:
        if Status.fpsUnlk_inst.poll() is None:
            Status.fpsUnlk_inst.terminate()
        Status.fpsUnlk_inst = None

    root.destroy()


root = Tk()
root.protocol("WM_DELETE_WINDOW", exit_handler)

root.title("Genshin Mod Launcher")
root.wm_geometry("300x250")
root.resizable(False, False)


centerFrm = ttk.Frame(root, padding=25)
centerFrm.place(relx=0.5, rely=0.5, anchor=CENTER)

in1 = EntryModified(centerFrm, width=25)
in1Txt = ttk.Label(centerFrm, text="3DMigoto Directory")
in1Txt.pack()
in1.pack()

in2 = EntryModified(centerFrm, width=25)
in2Txt = ttk.Label(centerFrm, text="FPS Unlocker Directory")
in2Txt.pack()
in2.pack()

runButton = Button(centerFrm, text="Run Genshin",command=lambda: runButton_handler(in1, in2))
runButton.pack(pady=10)

initialize_save_file_location(in1, in2)

root.mainloop()

