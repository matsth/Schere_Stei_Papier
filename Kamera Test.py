import pygame.camera
import pygame.image
import sys

pygame.camera.init()
camlist = pygame.camera.list_cameras()


cam = pygame.camera.Camera(camlist[0], (224, 224))

cam.start()


img  = cam.get_image()


WIDTH = img.get_width()
HEIGHT = img.get_height()

screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )

pygame.display.set_caption("pyGame Camera View")

while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()

    # draw frame
    screen.blit(img, (0,0))
    pygame.display.flip()
    # grab next frame    
    img = cam.get_image()
