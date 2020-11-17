import subprocess
from sys import version_info as vi
import tkinter as tk

root= tk.Tk()

canvas = tk.Canvas(root, width = 500, height = 400, bg = 'gray95', relief = 'raised')
canvas.pack()

def launch():
    try:
        subprocess.call("python ./main.py", shell=True, timeout=5)
    except subprocess.TimeoutExpired:
        pass

def createOptions():
    options = tk.Toplevel(root, width = 500, height = 400, bg = 'gray95', relief = 'raised')

    options.resizable(0, 0)
    options.title("Minecraft Python Options")
    options.iconphoto(False, icon) 
    options.geometry("500x400")

    def checkNumber(number):

        try:
            number = int(number)
        except:
            return False

        if(number > 0):
            return True
        return False


    def apply():
        open('options.txt', 'w').close()

        heightEntry = entryHeight.get()
        widthEntry = entryWidth.get()
        vsyncEntry = vsyncBool.get()

        if not checkNumber(heightEntry):
            heightEntry = 600

        if not checkNumber(widthEntry):
            widthEntry = 800

        file = open('options.txt', 'a')
        file.write(f"optionsHeight = {heightEntry}\n")
        file.write(f"optionsWidth = {widthEntry}\n")
        file.write(f"optionsVsync = {vsyncEntry}\n")
        file.close()

    vsyncBool = tk.BooleanVar()

    optionsTitle = tk.Label(options, text="Options Menu", font=('helvetica', 15, 'bold'))
    optionsDescription = tk.Label(options, text="Leave everything blank to reset to deafault.", font=('helvetica', 11, 'normal'))
    exitButton = tk.Button(options, text="Exit", command=options.destroy, bg='red', fg='white', font=('helvetica', 12, 'bold'))
    applyButton = tk.Button(options, text="Apply", command=apply, bg='blue', fg='white', font=('helvetica', 12, 'bold'))
    vsyncCheckbox = tk.Checkbutton(options, text="Enable Vsync", variable=vsyncBool, onvalue=True, offvalue=False)
    heightLabel = tk.Label(options, text="Height:")
    widthLabel = tk.Label(options, text="Width:")
    entryHeight = tk.Entry(options)
    entryWidth = tk.Entry(options)

    optionsTitle.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    optionsDescription.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    exitButton.place(relx=0.0, rely=0.0, anchor=tk.NW)
    applyButton.place(relx=1, rely=0, anchor=tk.NE)
    entryHeight.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
    heightLabel.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
    entryWidth.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
    widthLabel.place(relx=0.7, rely=0.4, anchor=tk.CENTER)
    vsyncCheckbox.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


launchButton = tk.Button(root, text='      Launch Minecraft: Python Edition    ', command=launch, bg='green', fg='white', font=('helvetica', 12, 'bold'))
exitButton = tk.Button(root, text="Exit", command=root.destroy, bg='red', fg='white', font=('helvetica', 12, 'bold'))
optionsButton = tk.Button(root, text="Options", command=createOptions, bg='blue', fg='white', font=('helvetica', 12, 'bold'))
mcVersion = tk.Label(root, text="Minecraft version: Alpha 1")
launchVersion = tk.Label(root, text="Launcher version: Alpha 1")
pythonVersion = tk.Label(root, text=f"Python version: {vi.major}.{vi.minor}.{vi.micro}")
mcTitle = tk.Label(root, text="Minecraft: Python Edition", font=('helvetica', 24, 'bold'))
icon = tk.PhotoImage(file ="textures/icon.png")

exitButton.place(relx=0.0, rely=0.0, anchor=tk.NW)
launchButton.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
optionsButton.place(relx=1, rely=0, anchor=tk.NE)
mcVersion.place(relx=0, rely=1, anchor=tk.SW)
launchVersion.place(relx=1, rely=1, anchor=tk.SE)
mcTitle.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
pythonVersion.place(relx=0.5, rely=1, anchor=tk.S)

canvas.create_window(150, 150)

root.resizable(0, 0)
root.title("Minecraft Python Launcher")
root.iconphoto(False, icon) 
root.geometry("500x400")

root.mainloop()