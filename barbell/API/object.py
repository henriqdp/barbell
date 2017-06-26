import pymunk

class Object:
    def __init__(self, barbell_instance):
        self.space = PymunkSpace().body_space(space,(constants.W_WIDTH/2, constants.W_HEIGHT/2 + constants.ROD_LENGTH), 60, 35)


    def update(self):
        pass
