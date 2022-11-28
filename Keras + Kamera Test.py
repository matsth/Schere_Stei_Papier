import pygame.camera
import pygame.image
import sys
import tensorflow
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageOps
import io
import time

import numpy as np


global model
file = r".\converted_keras\keras_model.h5"
model = keras.models.load_model(file, compile=False)

global size
size = (224, 224)

def GetPlayed(img):

    global model
    global size
    
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = img

    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)

    if(np.argmax(prediction) == 0):
        return 'Schere'
    elif(np.argmax(prediction) == 1):
        return 'Stein'
    elif(np.argmax(prediction) == 2):
        return 'Papier'

pygame.init()
pygame.camera.init()
camlist = pygame.camera.list_cameras()


cam = pygame.camera.Camera(camlist[0], size)

cam.start()

imggame  = cam.get_image()


WIDTH = imggame.get_width()
HEIGHT = imggame.get_height()

screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )

pygame.display.set_caption("pyGame Camera View")

font = pygame.font.SysFont(None, 48)

t_end = time.time()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not(time.time() < t_end):
        pil_string_image = pygame.image.tostring(imggame, "RGB", False)
        pli_image = Image.frombytes('RGB', imggame.get_size(), pil_string_image, 'raw')
        temp_io = io.BytesIO()
        pli_image.save(temp_io, "JPEG")

        resultMachine = GetPlayed(Image.open(temp_io))
        textsurface = font.render(resultMachine, True, (0, 0, 255))
        t_end = time.time() + 1
        
    # draw frame
    screen.blit(imggame, (0,0))
    screen.blit(textsurface, (20, 20))
    #pygame.display.flip()
    pygame.display.update()
    # grab next frame    
    imggame = cam.get_image()
    
pygame.quit()
