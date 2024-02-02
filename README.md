Instruction:

N:B: This source code uses the raylib GUI,and  can run both on windows and linux OS; to run on linux type:

        $   sudo  python3  main.py

  A video sample of the game is found at 


Source code Layout
 The game is designed with the help of three derived classes viz: "Part", "Tetromino" and "Game" in part.py, tetromino.py  and game.py respectively. The three classes are linked by composition and are described as follows:

1)              "Part"   class

Since a tetromino has four parts, this class was designed inoder to represent the (x,y)-axis value of each tetromino part as a single object. It overloads two special methods viz: __lt__  and __gt__  special methods.

__lt__ was overloaded in scenarios that require finding  the smaller of two object in terms of their x-axis value; thus usefull in applying the  sort()  and min() function to a list sequence of "Parts" objects.

__get__ special method was overloaded in scenario needed to get the larger of two objects in terms of their y-axis value; thus usefull when max() function is applied to a list sequence of "Part: objects.


2)              "Tetromino"   class

   This class generates the tetromino. A tetromino is a list sequence of "Part" objects, and each object represent the one of the four parts of a tetromino. It has two methods viz: "create_tromino() " and "clear_tetro()" , and are discussed below.

2.1 create_tetromino() : This method creates the tetromino; a tetromino and its color, is randomly selected from the "self.__shapes"   instance attribute and color list object. The selected shape and color is then returnedas a tuple.

2.2 clear_tetro:    This method is called before creating a new tetromino;it empties the "self.__tetro" instance prior to creating a new tetromino  



3)              "Game"  class

This class houses the body of the source code. It has 17 methods with some discussed below:

3.1     generate_new_tetromino
        This method generates a new tetromino each time it is called. It acheieves it objective by using the self.__tetro "Tetromino" object in caling the "create_tetro" method, and then assign the returned tuple to a tuple of "self.__tetromino" and "self.__tetromino_color".

3.2   place_boundary_condition
        This static method palces boundary condition on the game, and hence preventing the moving tetromino from leaving the canvas. It takes in three function arguements: ini_position, tetromino and direction representing the initial_position prior to moving to next position, "self.__tetromino" and "self.__direction" respectively. It acheives its objective as follows :

        step1 => get the part with the largest y-axis value
        step2 => get the two parts (one with least nad the other with the highest x-axis value)
        step3 => If result from step1 is greater than "GAME_HEIGHT - PIXEL_SIZE" return the entire tetromino to its previous position
        step4 => If the results from step3 is less than zero (if least) or greater than "GAME_WIDTH", return the entire tetromino back to its initial position.

3.3  label_board_reprica

        This method labels the 2D-list "self.__board_reprica". "self.__board_reprica" serves as a copy of the canvas. It is filled entire with zeros at start of game. "self.labell_board_reprica()" acheives its objectives through the steps:
        step 1 =>  loop through the four parts of the tetromino
        step 2 => get the x-axis and y-axis value of part "i"
        step3  =>  get the index position of results from  step2 in "self.__board_replicaX" and "self.__board_replicaY"
        step 4 => the index position the the x-axis and that of the y-axis value are the "column index" and " row index" respectively.
        step5 => assign a value of 1 in "self.__board_replica" at row "row_index" and column "column_index"
        step 6: move to the next part of the tetromino, and repeat steps 3 to 5.

3.4   break_down_tetromino_into_part

This method is uselfull so as to enable us completely separate the tetromino into independent parts. This is idea is important in scenarios where we want to delete a completely filled row from canvas, because a row consists of parts from different tetrominos. This method acheieves it objectives through the following steps:
        step1 => iterate through the four parts of the tetromino
        step 2 => append each part to the instance attribute "self.__all_obstructing_tetromino_parts"
        step 3 => since all parts of a tetromino share same color, append the color of the tetromino four times to the instance attribute "self.__all_obstructing_tetromino_parts_colors"

3.5 check_if_a_tetromino_is_ontop_another

        This method helps in vertical detection of collision. If any part of a tetromino lies ontop one of the obstructing parts it returns "True" else it returns "False". This method acheives its objective through the steps:
        step 1 => assume the tetromino moved forward. i.e get the next future position of the tetromino
        step2 => loop through the four parts of the tetromino at that future location
        step 3 => get the x-axis and y-axis value of part "i"
        step 4 => get the index position of the results from step3 in "self.__board_repricaX" and "self.__board_repricaY" respectively
        step 5 => check if "self.__board_reprica" is labelled aas 1 at the index positions obtained in step4
        step 5 => if step5 returns "True", then part "i" is ontop a part of an obstructing tetromino, because its future position is already occupied and hence the entire tetromino is ontop another.
        step 5 => if step 4 returns "False", check nex part "i+1"
        step 6 => If on checking all parts, and none has its immediate future position already occupied, then return "False". i.e the tetromino is not ontop another

3.6 check_if_tetromino_touch_another_by_the_side 

        This is a detects collision when a moving tetromino touches one of the obstructing parts by the side; thus prevent the tetromino from penetrating obstrucitng part. It acheives its objective through the following steps:

        step 1 => loop through the four parts of the moving tetromino
        step2  => get the  (x,y)-axis value for the part "i"
        step 3 => get the index positions of the two values obtained from step 2in "self.__board_replicaX" and "self.__board_replicaY" respectively.  the indexes obtained  are the "row_index" and "column_index" of part "i" on board replica
        step 4 => check if "self.__board_replica" has a value of 1 are such index, if yes, then return the entire tetromino back to it previous position
3.7  move_tetromino
        This method handles the stepwise movement of the tetromino. A tetromino can move "down", "left", "right" or "rotate". The tetromino moves down by default.  "self.move_tetromino()" acheives it objectives via the steps:
        step 1: assign the current position of the tetromino prioir to the varibale "initial_position". "initial_position" holds the current position of the tetromino prioir to movement
        step 2 => with the use of the match-case block, check for the value of "self.__direction".

        If "down", move the entire tetromino downwards by increasing the "y-axis" value of all its part while keeping the "x_axis" value constant. if the tetromino get to height "GAME_HEIGHT - PIXEL_SIZE", label board replica using "self.labell_board_replica()" method, breakdown the entire tetromino into parts and append them to "self.__all_obstructing_tetromino_parts" and finally generate a new tetromino

        If "left", move the tetromino left by substracting "PIXEL_SIZE" from the x-axis of all its four parts, but their y-axis value is kept constant. Check for boundary condition using the "self.__place_boundary_condtion" static method to prevent the tetromino from leaving the canvas

        if "right", move the entire tetromino right by adding "PIXEL_SIZE"to all the x-axis value of each of the four parts of the tetromino, but maintaining their y_axis value, and also place boundary detection.

        if "up", then rotate tetromino. tetromino is rotated via the steps:
        step 1 => select a centre of rotation
        step 2 => substract the (x,y)-axis value of all four parts from the centre chosen in step1
        step3 => invert the results by interchanging the the (x,y) values of each part. i.e
                        (x,y) = (y,x)

        step 4 => add the centre obtained from step1 to the result obtained from step 3.

3.8  delete_completely_filled_rows()

        This method deletes completely filled rows from the canvas. It acheives its objective through the steps:

        step 1 => starting from the last row, loop through "self.__board_replica"

        step 2 => check if row "i" is completely filled

        step 3 =>  if step 2 returns "True", increase the player's score by five, get the y-axis value of that row from "self.__board_replicaY" and append the value to "parts_to_delete"

        step 4 => starting the completely filled row of step2, assign the list-sequence of higher to that of lower row.

        step 5  =>  loop through "self.__all_obstructing_tetromino_parts" so as to get the parts

        step 6 =>  if the y-axis value of part "j" is found in "parts_to_delete", then delete(pop) that part from "self.__all_obstructing_tetromino_parts" and also its color from "self.__all_obstructing_tetromino_parts_colors".

        step 7 => obtain the maximum y-value present in "parts_to_delete"; this corresponds to the y-value of the last row deleted.

        step 8 =>  loop through "self.__all_obstructing_tetromino_parts" a second time, and check if the y-value of part "j" is lesser or equal to the result obtained from step 7 i.e if the part is found in a row lesser or equal to the last row that was deleted. This logic is salient in scenarios where the completely filled row in a canvas lies above an incompleley filled rows; hence only upper rows are moved downwards.

        step 9 => if step 8 returns true then that part is moved forward, otherwise it's kept at same location.

