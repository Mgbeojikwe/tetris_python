import tkinter as Tk
from tetromino import * 
import keyboard
import copy

class Game:

    def __init__ (self):

        self.__tetro= Tetromino()
        self.__tetromino=[]
        self.__tetromino_color=""

        self.__direction="down"

        self.__board_replicaX=[ i for i in range(0,GAME_WIDTH,PIXEL_SIZE)]                   #movement step of the tetromino in the x-axis
        self.__board_replicaY=[ i for i in range(0, GAME_HEIGHT, PIXEL_SIZE)]                #movement step of the tetromino  in the y-axis
        
        self.__board_replica=[ [0 for j in range(len(self.__board_replicaX))]  for i in range(len(self.__board_replicaY))]     #a board that represent the tetromino's movement on the canvas
        self.__board_replica_copy = copy.deepcopy(self.__board_replica)

        self.__all_obstructing_tetromino_parts=[]
        self.__all_obstructing_tetromino_parts_colors=[]

        self.__game_over = False

        #create the first tetromino once "Game" object is instantiated

        (self.__tetromino,self.__tetromino_color) = self.__tetro.create_tetro()



    def generate_new_tetromino(self):
        """
            This method generates a new tetromino. First it ensures that data represents the 
            previous tetromino are cleared proir to generating a new tetromino
        """

        self.__tetro.clear_tetro()
        (self.__tetromino, self.__tetromino_color ) = self.__tetro.create_tetro()


    @staticmethod
    def place_boundary_condition(ini_postion, tetromino, direction="down"):
        global GAME_HEIGHT
        """
            This method ensures that the tetromino does not leave the canvas by returning it to its previous position in scenarios
            where it current positions lies outside the canvas. With the help of the sort() and max() function, we obtain the tetromino
            parts that have the least x-axis, largest x-axis, and largest y-axis value, then we utilize ssuch in palcing boundary 
        """

        if (direction == "down"):
            
            
            tip = max(tetromino)

            if (tip.y >= GAME_HEIGHT):                 #If the tip of the tetromino is at "GAME_HEIGTH" value
                tetromino= ini_postion                  #return the tetromino back to "ini_position"

            else:
                 pass 
            

        else:                                           #if direction is "left" or "right"
            tetromino.sort()

            part_at_far_left = tetromino[0]
            part_at_far_right = tetromino[-1]

            if (part_at_far_left.x < 0  or part_at_far_right.x >= GAME_WIDTH):
                tetromino = ini_postion

            else:
                 pass

        return tetromino
    


    def labell_board_replica(self):

        """
            This method labels "self.__board_replica". Board replica is labelled based on the index position of the 
            the value of the (x,y)-component of each tetromino's part.

         """

        for part in self.__tetromino:
            x_axis_value = part.x
            y_axis_value = part.y

            #get the index of the (x,y)-componet of tetromino part "i", and use it to label board replica

            column_index =self.__board_replicaX.index(x_axis_value)
            row_index = self.__board_replicaY.index(y_axis_value)

            self.__board_replica[row_index][column_index] = 1   

    
    def break_down_tetromino_into_parts(self):
         """
            This method breaks down and obstructing tetromino into its separate parts. Since a tetromino has four
            parts of same color, the method also generate for similar colors for each parts.
            Finally this method returns a list of four parts and four colors.

         """

         for part in self.__tetromino:
              self.__all_obstructing_tetromino_parts.append(part)
         
         for i in range(4):
              self.__all_obstructing_tetromino_parts_colors.append(self.__tetromino_color)
        
    
    def check_if_tetromino_is_ontop_another(self):
         
         """
            This method checks if the current tetromino is ontop on one of the obstructing tetrominos. It acheives this 
            objective by checking if the future position of any of the tetromino parts has been occupied.

         
         """   
         future_position =list(map(lambda part:   Part(part.x, part.y+PIXEL_SIZE) , self.__tetromino))
         
         for part in future_position:
               x_axis_value = part.x
               y_axis_value = part.y

               column_index = self.__board_replicaX.index(x_axis_value)
               row_index = self.__board_replicaY.index(y_axis_value)

               if (self.__board_replica[row_index][column_index] == 1):
                     return True                                           # function ends if the future position of part "i" is occupied  
               
               else:
                     continue                                              #fi not check another part
          
         return False                                                      #return False if the no part has its future position already occupied

     

    def rotate_tetromino(self):
         
         
         """
            This method rotates the currently used tetromino
         """

         centre =  self.__tetromino[0]

         translated = list(map(lambda part: Part(part.x - centre.x, part.y - centre.y)  , self.__tetromino))
         
         inverted = list(map(lambda part:  Part(part.y, part.x) , translated))

         rotated_tetromino = list(map(lambda part: Part(part.x+centre.x, part.y + centre.y)   , inverted))
         
         self.__tetromino = rotated_tetromino


    def check_if_tetromino_touches_another_by_the_side(self, init_position):
         
         """
            This method ensures that a given tetromino does not pass-through an obstructing tetromino. 
            hence dectecting collision between a  moving tetromino and an obstructing tetromino. It achieves this objective
            by looping through all the parts of the tetromino, then searchin if the current position of a given part "i"
            has already been occupied. if yes, then the entire tetromino is returned to its intial state, and thus we break from the loop i.e no need
            searching for same condition in other parts 
         """
         
         for part in self.__tetromino:
              
                x_value = part.x
                y_value = part.y

                column_index = self.__board_replicaX.index(x_value)
                row_index = self.__board_replicaY.index(y_value)

                if (self.__board_replica[row_index][column_index] == 1):
                      self.__tetromino = init_position
                
                      break                             #since the position of one of the parts is already occupied
                                                        # return the entire tetromino to its initial state, and there is no
                                                        # search if other parts side-touche obstructing tetromino


    def move_tetromino(self):
       
       """
            This method moves the tetromino "down", "left" or "right" in steps of "PIXEL_SIZE". The stepwise "PIXEL_SIZE"
            is chosen so that the current position of the tetromino can be traced on "self.__board_reprica".

            "self.__board_replica" is only labelled when the tetromino reaches the canvas botton or when the tetromino is ontop
            another.
            if "self.__board_replica" is labelled, the tetromino studied is now known as "obstructing tetromino" and appended to 
            "self.__all_obstructing_tetromino_parts", and a new tetromino is generated

            "self.__board_replica"  is labelled if tetromino canvas game bottom or a tetromino is ontop another

            N:B:  Tetromino moves down by default
            """

       initial_position= self.__tetromino
       

       match (self.__direction):
           
           case "down":
               
               self.__tetromino = list(map(lambda part: Part(part.x , part.y + PIXEL_SIZE), self.__tetromino))

               self.__tetromino = self.place_boundary_condition(initial_position, self.__tetromino)   
               tetromino_tip = max(self.__tetromino)     

               if tetromino_tip.y == (GAME_HEIGHT-PIXEL_SIZE):# or self.check_if_tetromino_is_ontop_another() == True :# or self.check_if_tetromino_is_ontop_another() == True) :  #and self.tetromino_on_top_another == True :

                        self.labell_board_replica()
                        self.break_down_tetromino_into_parts()
                        self.generate_new_tetromino()

               if   self.check_if_tetromino_is_ontop_another() == True:
                            
                        self.labell_board_replica()
                        self.break_down_tetromino_into_parts()
                        self.generate_new_tetromino()

               else:
                    pass 

           
           case  "right":
                
                self.__tetromino = list(map(lambda part: Part(part.x + PIXEL_SIZE, part.y)  , self.__tetromino))

                self.__tetromino = self.place_boundary_condition(initial_position, self.__tetromino,"right")
                self.check_if_tetromino_touches_another_by_the_side(initial_position)

           case "left":
                 
                   self.__tetromino = list (map(lambda part: Part(part.x - PIXEL_SIZE, part.y)    , self.__tetromino))
                     
                   self.__tetromino = self.place_boundary_condition(initial_position,self.__tetromino, "left")
                   self.check_if_tetromino_touches_another_by_the_side(initial_position)
           
           case "up":

                 self.rotate_tetromino()

                 self.__tetromino = self.place_boundary_condition(initial_position,self.__tetromino,"up")     #placing boundary condition for scenarios where rotated tetromino parts
                                                                                                             #leaves the canvas

       self.__direction ="down"                                             #Tetromino will always move down by default    


    def delete_completely_filled_rows(self):
         """
               This method deltes completely filled row from the canvas. It does it by first
               checking if such row is completely filled in "self.__board_replica". It accepts no argument
         """

         global SCORE 
         parts_to_delete=[]

         last_index =len(self.__board_replica) -1
         
         for index in range(last_index,1,-1):

              row = self.__board_replica[index] 
              higher_row =self.__board_replica[index-1]

              row_is_completely_filled = all([ element ==  1 for element in row])
             
              if row_is_completely_filled == True:#  and higher_row_is_completely_filled == False:
                        SCORE +=5
                        
                        label.config(text=f"Score = {SCORE}")
                        y_value_of_affected_row = self.__board_replicaY[index]                 #get the y-axiz value of the affected row in order to delete 
                        parts_to_delete.append(y_value_of_affected_row)
                        
                        #moving every upper row downwards
                        for index2 in range(index,1,-1):
                              self.__board_replica[index2] = self.__board_replica[index2-1]

           
         
         if (len(parts_to_delete) >= 1):  
               largest_y_value = max(parts_to_delete)                                                  #if one or more rows were completely filled
            
               for index, part  in enumerate(self.__all_obstructing_tetromino_parts):

                         if part.y in parts_to_delete:
                         
                              self.__all_obstructing_tetromino_parts.pop(index)
                              self.__all_obstructing_tetromino_parts_colors.pop(index)

         
         #move each left over parts whose y_axis value is lesserthan or equal the 
          # y-axis value of the fist row deleted i.e the bottom downwards, in step of "PIXEL_SIZE"

               for index, part in enumerate(self.__all_obstructing_tetromino_parts):
                     
                         if part.y <= largest_y_value:
                               self.__all_obstructing_tetromino_parts[index] = Part(part.x, part.y + PIXEL_SIZE)

                         else:
                               continue 
                         
               # self.__all_obstructing_tetromino_parts = list(map(lambda part:  Part(part.x, part.y+PIXEL_SIZE) ,  self.__all_obstructing_tetromino_parts))
                  
         
    def print_tetromino_to_canvas(self):
         
         for part in self.__tetromino: 
              
             x = part.x
             y = part.y

             canvas.create_rectangle(x,y, x+PIXEL_SIZE-1, y+PIXEL_SIZE-1, fill=self.__tetromino_color, tags="tetromino")
    
    
    def print_all_obstructing_parts_to_canvas(self):

            for index,part in enumerate(self.__all_obstructing_tetromino_parts):

                    x = part.x
                    y = part.y     

                    color = self.__all_obstructing_tetromino_parts_colors[index]
                    canvas.create_rectangle(x,y,x+PIXEL_SIZE-1, y+PIXEL_SIZE-1, fill =color, tags="obstructing_part" )


    def game_over(self) :
         
         """
         Game ends if the second row in "self.__board_replica" has one or more 1
         """

         top_row = self.__board_replica[1]
         top_row_is_filled =any([ i == 1 for i in top_row])
    
         if top_row_is_filled == True:
                    
               self.__game_over = True  
          

    def change_direction(self, direction):
         self.__direction = direction

    
    def restart_key(self):

          if self.__game_over == True and self.__direction == "q":
               
               self.__game_over = False
               self.reset_game()


    def reset_game(self):
          global  SCORE
          
          SCORE= 0
          
          self.__all_obstructing_tetromino_parts.clear()
          self.__all_obstructing_tetromino_parts_colors.clear()
          self.__board_replica = copy.deepcopy(self.__board_replica_copy)                      #return "self.__board_replica" to its intial state

          self.generate_new_tetromino()

    def bind(self):
         
         
          if self.__game_over == True:
                self.print_all_obstructing_parts_to_canvas()
                canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("consolas",70), text="GAME  OVER", fill="red")
                canvas.create_text( canvas.winfo_width()/2, canvas.winfo_height()-(3*PIXEL_SIZE), font=("consolas",22), text="Hit q to restart game", fill="green")
                
                #self.print_all_obstructing_parts_to_canvas()
          
          else:                
               window.bind("<Left>", lambda x: self.change_direction("left"))    

               window.bind("<Right>", lambda x: self.change_direction("right"))

               window.bind("<Up>", lambda x: self.change_direction("up"))

               window.bind("<Down>", lambda x: self.change_direction("down"))

               window.bind("<q>", lambda x: self.change_direction("q"))


    def play(self):

            canvas.delete("all")

            if self.__game_over == False:
                 
                 self.move_tetromino()
                 self.delete_completely_filled_rows()
                 self.print_all_obstructing_parts_to_canvas()
                 self.print_tetromino_to_canvas()
                 self.game_over()
                 self.bind()
                 
            
            else:
                    self.restart_key()
                    self.bind()
                    

            canvas.after(GAME_SPEED, self.play)


window=Tk.Tk()
window.title("Tetris")
window.resizable(False,False)
label=Tk.Label(window, text=f"score={SCORE}", font=("consolas",40))
label.pack()

canvas=Tk.Canvas(window, bg=BACK_GROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
window.update()
