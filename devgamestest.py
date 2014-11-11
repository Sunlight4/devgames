import pygame
import devgames
from devgames import main, util
from devgames.vector import Vector
devgames.newvital("You Lose!")
class KeyboardSquareBlock(util.KeyboardControlledObject, util.SquareBlock):pass
block1=KeyboardSquareBlock((255,0,0), 32, 320, 100)
block2=util.SquareBlock((0,0,255), 32, 200, 50)
block1.killoncontact(block2)
devgames.vital[0][0].add(block1)
main({}, {}, block1, block2)
pygame.quit()
