'''Simple splash screen for Chrome'''

import Tkinter as tk
import subprocess
import time
import threading

def checkRunning():
    found = False
    while not found:
        try:
            subprocess.check_call('tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I /N "chrome.exe">NUL', shell=True) #throws an exception when chrome is found
            time.sleep(1)
        except:
            found = True
            root.after(1*1000, root.destroy) #it takes some time for chrome to start up

root = tk.Tk()
root.overrideredirect(True)

image = tk.PhotoImage(file="chrome.gif")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (image.width(), image.height(), (width-image.width())/2, (height-image.height())/2))

canvas = tk.Canvas(root, height=image.height(), width=image.width(), bg="black")
canvas.create_image(image.width()/2, image.height()/2, image=image)
canvas.pack()

subprocess.Popen("GoogleChromePortable.exe")
threading.Thread(target=checkRunning).start()

root.mainloop()
