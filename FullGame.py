import sys
import io
import time
import math
import random as rng
import numpy as np
from PIL import Image, ImageOps
import pygame.camera
import pygame.image
import tensorflow
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator


#AI
#------------------------------------------------------------------
global aichoice
global aibehaviorlearning
global aibehavior

learningfactorwin = 3
learningfactorlose = -3
learningfactordraw = -1

#Set up AI Array
#0 = Random()
#1 = Copycat()
#2 = Winlast()
#3 = Counterlose()
#4 = CounterCounterwin()
#5 = Countermosteplayed()
aibehaviorlearning = np.array([1, 60, 60, 60, 60, 60])

aibehavior = 0

#AIinfos
#------------------------------------------------------------------
global userchoice
global lastwon
global moveused

moveused = np.array([0, 0, 0])
lastwon = None

#Import Model and set size of img
#------------------------------------------------------------------
global model
file = r".\converted_keras\keras_model.h5"
model = keras.models.load_model(file, compile=False)

global size
size = (224, 224)
size2 = (448, 448)

#Rest
#------------------------------------------------------------------
aiWins = 0
playerWins = 0
draws = 0

#0 = Schere
#1 = Stein
#2 = Papier
numbertonamearr = ['Schere', 'Stein', 'Papier']


#AI behavior
#------------------------------------------------------------------
#Random Choice of Counter
def Random():
    global aichoice
    aichoice = rng.randint(0,2)

#Copy the move of the Oponent
def Copycat():
    global aichoice
    global userchoice

    aichoice = userchoice

#Counter last move of oponent
def Winlast():
    global aichoice
    global userchoice

    match userchoice:
        case 0:
            aichoice = 1
        case 1:
            aichoice = 2
        case 2:
            aichoice = 0

#Counter the move that would lose aiganst the last enemy played move
def Counterlose():
    global aichoice
    global userchoice

    match userchoice:
        case 0:
            aichoice = 2
        case 1:
            aichoice = 0
        case 2:
            aichoice = 1

#Counter the Counter of what last won
def CounterCounterwin():
    global aichoice
    global aibehavior
    global lastwon
    
    if not(lastwon == None):
        match lastwon:
            case 0:
                aichoice = 2
            case 1:
                aichoice = 0
            case 2:
                aichoice = 1
        
    else:
        Random()
        aibehavior = 0

#Counter what your oponent plays most
def Countermosteplayed():
    global aichoice
    global moveused

    if(moveused[0] > moveused[1]):
        if(moveused[0] > moveused[2]):
            aichoice = 1
        else:
            aichoice = 0
    else:
        if(moveused[1] > moveused[2]):
            aichoice = 2
        else:
            aichoice = 0

#AI learning
#------------------------------------------------------------------
def AIlearning(modi):
    global aibehavior
    global aibehaviorlearning

    
    aibehaviorlearning[aibehavior] += modi

    if not(aibehaviorlearning[aibehavior] >= 1):
        aibehaviorlearning[aibehavior] = 1

    if(aibehaviorlearning[0] > 1):
        aibehaviorlearning[0] = 1

def ChooseAI():
    global aibehaviorlearning
    global aibehavior

    x = rng.randint(1, np.sum(aibehaviorlearning))

    if(x <= aibehaviorlearning[0]):
        Random()
        aibehavior = 0
    elif(x <= aibehaviorlearning[0] + aibehaviorlearning[1]):
        Copycat()
        aibehavior = 1
    elif(x <= aibehaviorlearning[0] + aibehaviorlearning[1] + aibehaviorlearning[2]):
        Winlast()
        aibehavior = 2
    elif(x <= aibehaviorlearning[0] + aibehaviorlearning[1] + aibehaviorlearning[2] + aibehaviorlearning[3]):
        Counterlose()
        aibehavior = 3
    elif(x <= aibehaviorlearning[0] + aibehaviorlearning[1] + aibehaviorlearning[2] + aibehaviorlearning[3] + aibehaviorlearning[4]):
        CounterCounterwin()
        aibehavior = 4
    else:
        Countermosteplayed()
        aibehavior = 5

#Model recognize img
#------------------------------------------------------------------
def MoveinImg(img):

    global model
    global size
    
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = img

    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)

    return np.argmax(prediction)

#Set up pygame Screen
#------------------------------------------------------------------
pygame.init()
pygame.camera.init()
camlist = pygame.camera.list_cameras()


cam = pygame.camera.Camera(camlist[0], size2)

cam.start()

imggame  = cam.get_image()


WIDTH = imggame.get_width()
HEIGHT = imggame.get_height()

screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )

pygame.display.set_caption("pyGame Camera View")

font = pygame.font.SysFont(None, 44)

font2 = pygame.font.SysFont(None, 28)

#Game
#------------------------------------------------------------------
Random()
leave = 0
error = 0
result = ''
textevent = font2.render(result, True, (0, 0, 255))

t_offset = 0.1
t_offset2 = 5

t_end = time.time()
t_end2 = time.time() + t_offset2

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #User Input wird gelesen
    if (time.time() >= t_end):
        pil_string_image = pygame.image.tostring(imggame, "RGB", False)
        pli_image = Image.frombytes('RGB', imggame.get_size(), pil_string_image, 'raw')
        temp_io = io.BytesIO()
        pli_image.save(temp_io, "JPEG")

        resultMachine = MoveinImg(Image.open(temp_io))

        error = 0
        if(resultMachine == 0):
            userchoice = 0
            resultMachinetext = 'Schere'
            t_end = time.time() + t_offset
        elif(resultMachine == 1):
            userchoice = 1
            resultMachinetext = 'Stein'
            t_end = time.time() + t_offset
        elif(resultMachine == 2):
            userchoice = 2
            resultMachinetext = 'Papier'
            t_end = time.time() + t_offset
        else:
            error = 1
            resultMachinetext = 'Ungültige eingabe!'
        
        textsurface = font.render(resultMachinetext, True, (0, 0, 255))

    #Actual Game
    if (error < 1 and time.time() >= t_end2):
        match aichoice:
            case 0:
                match userchoice:
                    case 0:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' unentschieden!'
                        moveused[userchoice] += 1
                        draws += 1
                        AIlearning(learningfactordraw)
                    case 1:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' Du gewinnst!'
                        moveused[userchoice] += 1
                        playerWins += 1
                        lastwon = userchoice
                        AIlearning(learningfactorlose)
                    case 2:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' KI gewinnst!'
                        moveused[userchoice] += 1
                        aiWins += 1
                        lastwon = aichoice
                        AIlearning(learningfactorwin)
            case 1:
                match userchoice:
                    case 0:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' KI gewinnst!'
                        moveused[userchoice] += 1
                        aiWins += 1
                        lastwon = aichoice
                        AIlearning(learningfactorwin)
                    case 1:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' unentschieden!'
                        moveused[userchoice] += 1
                        draws += 1
                        AIlearning(learningfactordraw)
                    case 2:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' Du gewinnst!'
                        moveused[userchoice] += 1
                        playerWins += 1
                        lastwon = userchoice
                        AIlearning(learningfactorlose)
            case 2:
                match userchoice:
                    case 0:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' Du gewinnst!'
                        moveused[userchoice] += 1
                        playerWins += 1
                        lastwon = userchoice
                        AIlearning(learningfactorlose)
                    case 1:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' Ki gewinnst!'
                        moveused[userchoice] += 1
                        aiWins += 1
                        lastwon = aichoice
                        AIlearning(learningfactorwin)
                    case 2:
                        result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' unentschieden!'
                        moveused[userchoice] += 1
                        draws += 1
                        AIlearning(learningfactordraw)

        ChooseAI()
        t_end2 = time.time() + t_offset2
        
        textevent = font2.render(result, True, (0, 0, 255))

    timetext = font.render(str(math.ceil(t_end2 - time.time())), True, (0, 0, 255))
    # draw frame
    screen.blit(imggame, (0,0))
    screen.blit(textsurface, (20, 20))
    screen.blit(timetext, (520, 20))
    screen.blit(textevent, (20, 320))
    #pygame.display.flip()
    pygame.display.update()
    # grab next frame    
    imggame = cam.get_image()

print('AI wins: ' + str(aiWins))
print('Player wins: ' + str(playerWins))
print('Draws: ' + str(draws))
print('Random(): ' + str(aibehaviorlearning[0]))
print('Copycat(): ' + str(aibehaviorlearning[1]))
print('Winlast(): ' + str(aibehaviorlearning[2]))
print('Counterlose(): ' + str(aibehaviorlearning[3]))
print('CounterCounterwin(): ' + str(aibehaviorlearning[4]))
print('Countermosteplayed(): ' + str(aibehaviorlearning[5]))
print(numbertonamearr[0] + ': ' + str(moveused[0]))
print(numbertonamearr[1] + ': ' + str(moveused[1]))
print(numbertonamearr[2] + ': ' + str(moveused[2]))
pygame.quit()
