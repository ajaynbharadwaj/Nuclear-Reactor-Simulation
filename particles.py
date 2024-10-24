import numpy as np

class atom():
    
    def __init__(self, x, y, ATOM_RADIUS, element):
        self.radius = ATOM_RADIUS
        self.uranium = element
        self.x = x
        self.y = y

        if self.uranium:
            self.color = (50,100,200)
        else:
            self.color = (150,150,150)

class neutrino():

    def __init__(self, x, y, NEUTRINO_RADIUS, angle, velocity):
        self.x = x
        self.y = y
        self.radius = NEUTRINO_RADIUS
        self.angle = angle
        self.velocity = velocity
        self.color = (0,0,0)

    def posUpdate(self):
        self.x += self.velocity * np.cos(np.deg2rad(self.angle))
        self.y += self.velocity * np.sin(np.deg2rad(self.angle))