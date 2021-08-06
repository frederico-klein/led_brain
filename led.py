# import the pygame module, so you can use it
import sys
import pygame
import logging
from pygame.locals import *
import random, itertools #this is only here for testing!!!!

from dia import *

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

pygame.init()

# Assign FPS a value
FPS = 60
FramePerSec = pygame.time.Clock()

# Setting up color objects
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

GAME_FONT = pygame.font.Font("DejaVuSans.ttf", 10)
SMALL_FONT = pygame.font.Font("DejaVuSans.ttf", 8)

NUM_OF_LEDS = 800

DIGITS_TO_DISPLAY = len(str(NUM_OF_LEDS))

class LedArray():
    def __init__(self, arrays= []):
        self.arrays = arrays
        self.usedleds = []
        self._checkarr()

    def _checkarr(self):
        self.usedleds = []
        for arr in self.arrays:
            for led in arr.LEDs:
                if led.index in self.usedleds:
                    logging.warning("led collision (%d). using a random set to reinitialize led_seq for array: %s"%(led.index), arr.name))
                    remainingleds = set(set(range(NUM_OF_LEDS))-set(self.usedleds))
                    #arr.led_seq = random.sample(remainingleds, arr.num_leds)
                    led_seq = [i for i in itertools.islice(remainingleds, arr.num_leds)]
                    arr.update(led_seq = led_seq)
                    logging.debug("new led_seq for array: %s"%arr.led_seq())
            self.usedleds.extend(arr.led_seq())
        for arr in self.arrays:
            arr.draw()

    def reg(self, arr):
        self.arrays.append(arr)
        self._checkarr()

    def set_led(self, led, color):
        led_in_array = []
        for led_array in self.arrays:
            if led>0 and led in led_array.led_seq:
                led_array.set(led,color)
                logging.debug("LED: %d found in %s"%(led, led_array.name))
                led_in_array.append(led_array)
        if len(led_in_array)>1:
            arr_names = str([arr.name for arr in led_in_array])
            logging.error("LED in %s"%arr_names)
            raise Exception("Led found in multiple arrays")
        if not led_in_array:
            raise Exception("Led not found")


class TextBoxy():
    def __init__(self, canvas,  p1,p2,p3=100,p4=50, color = RED, textcolor = BLACK):
        self.pos = (p1,p2)
        self.canvas = canvas
        self.color = color
        self.textcolor = textcolor
        #self.rect = Rect(50, 60, 200, 80)
        self.rect = Rect(p1,p2,p1+p3,p2+p4)

    def mess(self, message):
        debugpane =  GAME_FONT.render( message, True, self.textcolor)
        self.canvas.blit(debugpane, self.pos)

    def white(self):
        pygame.draw.rect(self.canvas, self.color, self.rect)

# define a main function
def main():

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("LED brain visualization")


    # create a surface on screen
    screen = pygame.display.set_mode((1400,800))
    screen.fill(WHITE)
    prefrontalarrayL = LedBlock(0,0  , 3, 4, canvas = screen, name="Pre-frontal Left" , led_seq=[2,3,4,5,6,7,8,41,9,10,11,1])
    prefrontalarrayR = LedBlock(0,340, 3, 4, canvas = screen, name="Pre-frontal Right", led_seq=[12,13,14,15,16,17,18,42,19,20,21,22])

    fronttemporoparietalarrayL = LedBlock(200,0  , 30, 10, canvas = screen, name="Fronto Temporo Parietal Left")
    fronttemporoparietalarrayR = LedBlock(200,340, 30, 10, canvas = screen, name="Fronto Temporo Parietal Right")

    occiptL = LedBlock(1200,0  , 4, 6, canvas = screen, name="Occipital Left")
    occiptR = LedBlock(1200,340, 4, 6, canvas = screen, name="Occipital Left")

    aLa = LedArray([prefrontalarrayL, prefrontalarrayR, fronttemporoparietalarrayL, fronttemporoparietalarrayR , occiptL, occiptR  ])

    #my gray erase rectangle
    rect = TextBoxy(screen, 40,700)



    # main loop
    while True:
        message = "Debug: "
        rect.white()
        raisedClick = False

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                on_closing()
                return

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                message+= str(pos)
                raisedClick = True
                #answer = mydialog(app)
                # print(type(answer)) # tuple
                #print(answer)

        rect.mess(message)

        FramePerSec.tick(FPS)

        prefrontalarrayL.set(2,RED)
        prefrontalarrayL.set(41,GREEN)
        prefrontalarrayL.set(3,BLUE)
        prefrontalarrayL.set(4,RED)
        prefrontalarrayL.set(5,GREEN)

        prefrontalarrayL.set(10,BLUE)

        aLa.set_led(12,GREEN)
        aLa.set_led(42,BLUE)
        aLa.set_led(1,RED)

        pygame.display.update()

        if raisedClick:
            answer = mydialog(app)
            logging.info(answer)
        try:
            app.update()
        except:
            pass

class LED():
    def __init__(self, index = 0, color = (0,0,0), enabled = True, pos = (0,0), size = 20, parent_block = None):
        self.index = index
        self.color = color
        self.enabled = enabled
        self.pos = pos
        self.size = size
        self.parent_block = parent_block
        try:
            self.canvas = parent_block.canvas
        except:
            self.canvas = None
            logging.warning("No canvas set for LED %d"%self.index)

    def set(self, index,  color = GRAY, enabled = True):
        if self.index != index:
            logging.warning("changed index of LED %d to %d"%(self.index, index))
            self.index = index
        self.color = color
        self.enabled = enabled
        if not self.enabled:
            logging.warning("The formerly LED %d is now disabled."%self.index)
            self.index = -1
            self.color = GRAY

        ### the showing part
        pygame.draw.circle(self.canvas, self.color , self.pos, self.size/2)
        if self.enabled:
            thisx, thisy = self.pos
            text_surface = SMALL_FONT.render( str(self.index).zfill(DIGITS_TO_DISPLAY), True, BLACK)
            self.canvas.blit(text_surface, (thisx-(DIGITS_TO_DISPLAY*2+1), thisy-5))


class LedBlock():

    def __init__(self, x,y,nx=1,ny=1, led_spacing=10, led_size=20, canvas=pygame.display.set_mode((400,200)), led_seq=[], name="Unnamed Array"):#, canvas=screen):
        self.origin = (x,y)
        self.name = name
        self.n = (nx,ny)
        self.num_leds = nx*ny
        self.led_size = led_size
        self.led_spacing = led_spacing
        self.canvas = canvas
        text_surface = GAME_FONT.render( self.name, True, BLACK)
        canvas.blit(text_surface, self.origin)
        if not led_seq:
            logging.warning("Led sequence not informed. Using default")
            _led_seq = range(nx*ny)
        else:
            assert(len(led_seq) == nx*ny)
            _led_seq = led_seq
        self.update(led_seq = _led_seq)

    def update(self, led_seq = []):
        self.LEDs = []
        for led in led_seq:
            i,j,k = self.iterate(led)
            center = self.led_center(i,j)

            self.LEDs.append(LED(index=led, color = GRAY, pos = center, size = self.led_size, parent_block = self))

    def led_center(self, i, j):
        thisx = self.origin[0]+self.led_size/2*(1+2*i)+self.led_spacing*i
        thisy = self.origin[1]+self.led_size/2*(1+2*j)+self.led_spacing*j+20#some offset
        return thisx,thisy

    def iterate(self, led_index):
        k = -1
        for kk, led in enumerate(self.LEDs):
            if led_index == led.index:
                k = kk
                break

        #k = self.led_seq.index(led_index)
        i= k%self.n[0]
        j= k//self.n[0]
        logging.debug("i:%d, j:%d, k:%d"%(i,j,k))
        return i,j,k

    def draw(self):
        for led in self.LEDs:
            led.set(led.index, GRAY)

    def set(self, led_index, color):
        for aLed in self.LEDs:
            if led_index == aLed.index:
                aLed.set(led_index, color = color)

    def led_seq(self):
        led_seq = []
        for aLed in self.LEDs:
            led_seq.append(aLed.index)

        return led_seq
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    try:
        main()
    except KeyboardInterrupt:
        pass
