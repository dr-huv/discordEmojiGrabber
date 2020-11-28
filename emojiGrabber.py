import win32clipboard
import string
import random
import time
import os
import requests
from PIL import Image

recentValue = ''

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
    r = requests.get(getClipboard())
    with open(destination, 'wb') as f:
        f.write(r.content)    
    image = Image.open(destination) # I have combined the function that downloads the image and resizes the image because due to getRandomFileName, it would change value as soon as its called a second time
    image = image.resize((48, 48), Image.ANTIALIAS)
    image.save(destination)
#to resize an image
        
clipboardData = getClipboard() 

while True:
    if recentValue != getClipboard(): #this is to check if some new link has been copied
        recentValue = getClipboard()
        getRandomFileName()
        createResizedImage()
        print("Image processing done")
    time.sleep(0.4) # if this statement wasnt included, the program would consume all of the CPUs memeory, so the while statement now happens once every 0.4s
