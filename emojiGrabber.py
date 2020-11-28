import win32clipboard
import string
import random
import time
import os
import requests
from PIL import Image

recentValue = ''

#to create the directory if it doesn't already exist
def directorycheck():
    destination  = os.path.join(os.environ.get("USERPROFILE") , "Desktop" , "Discord emojis")
    if not (os.path.isdir(destination)):
        os.mkdir(destination)

directorycheck()

#to get the value from the clipboard
def getClipboard():
    win32clipboard.OpenClipboard()
    clipboardData = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return clipboardData

#to get a random name for the file
def getRandomFileName():
    fileDestList = [] #created this list so that i can pass both the file destination and file name in the return statement
    letters = string.ascii_lowercase #this is actually a string of all the lowercase letters
    fileName = ''.join((random.choice(letters)) for i in range(8))
    destination  = os.path.join(os.environ.get("USERPROFILE") , "Desktop" , "Discord emojis", fileName + ".png")
    fileDestList.append(fileName)
    fileDestList.append(destination)
    return fileDestList

#to write the file we obtain from the clipboardData
def createResizedImage():
    fileName  = getRandomFileName()[0]
    destination = getRandomFileName()[1]
    try:
        r = requests.get(getClipboard())
        with open(destination, 'wb') as f:
            f.write(r.content)    
        image = Image.open(destination) # I have combined the function that downloads the image and resizes the image because due to getRandomFileName, it would change value as soon as its called a second time
        image = image.resize((48, 48), Image.ANTIALIAS)
        image.save(destination)
        status = 'Image processing done'
    except:
        print("lmao, try copying an image url next time")
        status = 'Image processing Failed'
    
    return status
#to resize an image
    
clipboardData = getClipboard() 

while True:
    if recentValue != getClipboard(): #this is to check if some new link has been copied
        recentValue = getClipboard()
        getRandomFileName()
        status = createResizedImage()
        print(status)
    time.sleep(0.4) # if this statement wasnt included, the program would consume all of the CPUs memeory, so the while statement now happens once every 0.4s
