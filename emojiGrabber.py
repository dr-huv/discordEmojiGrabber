import string
import random
import time
import os
import requests
from PIL import Image
from colorama import Fore, Back, Style, init

init(convert=True)

recentValue = ""
home = "" # linux and mac have the env variable HOME instead of USERPROFILE, this will point to the home directory

platform = os.name

if platform == "nt":
    import win32clipboard
    home = os.environ.get("USERPROFILE")
    
else:
    import subprocess
    home = os.environ.get("HOME")

# to create the directory if it doesn't already exist
def directorycheck():
    destination = os.path.join(home, "Desktop", "Discord emojis")
    if not (os.path.isdir(destination)):
        os.mkdir(destination)


directorycheck()

# to get the value from the clipboard
def getClipboard():
    if platform == "nt":
        win32clipboard.OpenClipboard()
        clipboardData = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return clipboardData

    else:
        p = subprocess.Popen(
            ["xclip", "-selection", "clipboard", "-o"], stdout=subprocess.PIPE
        )
        retcode = p.wait()
        clipboardData = p.stdout.read()
        return str(clipboardData).split("'")[1]


# to get a random name for the file
def getRandomFileName():
    fileDestList = (
        []
    )  # created this list so that i can pass both the file destination and file name in the return statement
    letters = (
        string.ascii_lowercase
    )  # this is actually a string of all the lowercase letters
    fileName = "".join((random.choice(letters)) for i in range(8))
    destination = os.path.join(
        home, "Desktop", "Discord emojis", fileName + ".png"
    )
    fileDestList.append(fileName)
    fileDestList.append(destination)
    return fileDestList


# to write the file we obtain from the clipboardData
def createResizedImage():
    fileName = getRandomFileName()[0]
    destination = getRandomFileName()[1]
    try:
        r = requests.get(getClipboard())
        with open(destination, "wb") as f:
            f.write(r.content)
        image = Image.open(
            destination
        )  # I have combined the function that downloads the image and resizes the image because due to getRandomFileName, it would change value as soon as its called a second time
        image = image.resize((48, 48), Image.ANTIALIAS)
        image.save(destination)
        status = "Image processing done"
    except:
        print(Fore.RED + "lmao, try copying an image url next time")
        status = "Image processing Failed"

    return status


# to resize an image

clipboardData = getClipboard()

while True:
    if (
        recentValue != getClipboard()
    ):  # this is to check if some new link has been copied
        recentValue = getClipboard()
        if (
            "discord" in recentValue and "png" in recentValue
        ):  # This makes sure, that the code is run only when a discord emoji link is copied and not everytie the clipboard changes value lol
            getRandomFileName()
            status = createResizedImage()
            if "failed" in status:
                print(Fore.RED + status)
            else:
                print(Fore.GREEN + status)
    time.sleep(
        0.4
    )  # if this statement wasnt included, the program would consume all of the CPUs memeory, so the while statement now happens once every 0.4s
