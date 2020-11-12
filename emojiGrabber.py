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
    fileDestList = []
    letters = string.ascii_lowercase
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
    image = Image.open(destination)
    image = image.resize((48, 48), Image.ANTIALIAS)
    image.save(destination)
#to resize an image
        
clipboardData = getClipboard()

# print(clipboardData)

# print(getRandomFileName())
# print(getRandomFileName())

#if recentValue != clipboardData:
# createImage()
# resizeImage()    

while True:
    if recentValue != getClipboard():
        recentValue = getClipboard()
        getRandomFileName()
        createResizedImage()
        print("Image processing done")
    time.sleep(0.4)