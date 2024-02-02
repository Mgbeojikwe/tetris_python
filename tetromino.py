import random
from part import *

PIXEL_SIZE=40
GAME_WIDTH= 20*PIXEL_SIZE
GAME_HEIGHT= 20*PIXEL_SIZE
SCORE=0
BACK_GROUND_COLOR="#000000"
GAME_SPEED=150

class Tetromino:


    def __init__(self):

        self.__tetro=[]

    def create_tetro(self):

        """
        This method creates the tetro. its shape and color is randmly selected from "shapes" and "colors" objects.
        The tetro and its color are returned
        """
        possible_starting_x_value = [i for i in range(0, GAME_WIDTH,PIXEL_SIZE)]
        index= len(possible_starting_x_value)//2
        start_x = possible_starting_x_value[index]
        start_y= 0

        shapes=["L","box","I","N","T",]
        colors=["#0000FF","#ED9121","#D2691E","#4B0082","#FF8000","#7CCD7C","#FFFAFA","#FFFF00"]


        choice=random.choice(shapes)

        match (choice):

            case "L":
                self.__tetro=[ Part(start_x, start_y), Part(start_x, start_y+PIXEL_SIZE), Part(start_x, start_y+(2*PIXEL_SIZE)), Part(start_x+PIXEL_SIZE, start_y+(2*PIXEL_SIZE))]
            
            case "N":

                self.__tetro = [ Part(start_x+PIXEL_SIZE,start_y), Part(start_x+PIXEL_SIZE, start_y+PIXEL_SIZE), Part(start_x, start_y+PIXEL_SIZE), Part(start_x,start_y+(2*PIXEL_SIZE))]
            
            case "box":
                self.__tetro = [Part(start_x, start_y), Part(start_x+PIXEL_SIZE, start_y), Part(start_x,start_y +PIXEL_SIZE), Part(start_x+PIXEL_SIZE, start_y+PIXEL_SIZE)]
            
            case  "T":

                self.__tetro = [ Part(start_x + PIXEL_SIZE,start_y), Part(start_x, start_y+PIXEL_SIZE), Part(start_x+PIXEL_SIZE,start_y+PIXEL_SIZE), Part(start_x+(2*PIXEL_SIZE), start_y+PIXEL_SIZE)]
            
            case "I":

                self.__tetro = [Part(start_x, start_y), Part(start_x, start_y+PIXEL_SIZE), Part(start_x,start_y+(2*PIXEL_SIZE)), Part(start_x, start_y+(3*PIXEL_SIZE))] 
        
        
        tetro_color =random.choice(colors)                              #randomly selecting tetromino color

        return (self.__tetro, tetro_color)


    def clear_tetro(self):

        """
        This method empties "self.__tetro". It is import in scenarios where we need to create subsequent tetros.
        """
        self.__tetro.clear()
