


class Part:


    def __init__ (self, x_axis_value, y_axis_value):

        self.x = x_axis_value
        self.y = y_axis_value

    def __lt__ (self, rhs):
        """
        This special method is called in scenarios that require comparing the x-axia value of two "Part" objects; thus 
        import in scenarios that involve the use of sort() and min() functions on a list sequence of "Part" objects.
        """
        
        return self.x < rhs.x
    
    def __gt__(self, rhs):
        """
            This special method gets the larger of two "Part" objects based on their y-axis values. This method is 
            import in scenarios that involves applying the max() function to a list sequence of "Part" objects
            inorder to obtain the object with the largest y-axis value
        """
        return self.y > rhs.y