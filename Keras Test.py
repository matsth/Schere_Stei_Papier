import tensorflow
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageOps
import glob
import numpy

numpy.set_printoptions(suppress=True)

file = r".\converted_keras\keras_model.h5"

global model
model = keras.models.load_model(file, compile=False)

imageS = Image.open(r".\Schere.jpg")
imageR = Image.open(r".\Stein.jpg")
imageP = Image.open(r".\Papier.jpg")

def getPlayer(img):

    global model

    data = numpy.ndarray(shape=(1, 224, 224, 3), dtype=numpy.float32)

    image = img

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = numpy.asarray(image)

    normalized_image_array = (image_array.astype(numpy.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)

    print(numpy.argmax(prediction))

getPlayer(imageS)
getPlayer(imageR)
getPlayer(imageP)
