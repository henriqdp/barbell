import pymunk

class PymunkSpace():
    def body_space(self, space, position, mass, radius):
        self.space = space
        self.mass = mass
        self.radius = radius
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, self.inertia)
        self.body.position = position
        # self.shape = pymunk.Circle(self.body, self.radius)
        self.space.add(self.body, self.shape)
        return self.shape
