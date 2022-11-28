import pygame.camera
import pygame.image
import sys
import tensorflow
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageOps
import io

import numpy


global model
file = r".\converted_keras\keras_model.h5"
model = keras.models.load_model(file, compile=False)

global size
size = (224, 224)

def GetPlayed(img):

    global model
    global size
    
    data = numpy.ndarray(shape=(1, 224, 224, 3), dtype=numpy.float32)

    image = img

    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = numpy.asarray(image)

    normalized_image_array = (image_array.astype(numpy.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)

    print(numpy.argmax(prediction))


pygame.camera.init()
camlist = pygame.camera.list_cameras()


cam = pygame.camera.Camera(camlist[0], size)

cam.start()

imggame  = cam.get_image()


WIDTH = imggame.get_width()
HEIGHT = imggame.get_height()

screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )

pygame.display.set_caption("pyGame Camera View")

while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()

    pil_string_image = pygame.image.tostring(imggame, "RGB", False)
    pli_image = Image.frombytes('RGB', imggame.get_size(), pil_string_image, 'raw')
    temp_io = io.BytesIO()
    pli_image.save(temp_io, "JPEG")
    GetPlayed(Image.open(temp_io))

        
    # draw frame
    screen.blit(imggame, (0,0))
    pygame.display.flip()
    # grab next frame    
    imggame = cam.get_image()

