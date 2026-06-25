import math
from neo_detect.abs_mag import Asteroid

class Phase_Function:
    def __init__(self, angle: float, G: float = 0.15):
        self.angle = angle
        self.G = G

    def phase_function(self):
        phi1 = math.exp(-3.33 * (math.tan(math.radians(self.angle / 2))) ** 0.63)
        phi2 = math.exp(-1.87 * (math.tan(math.radians(self.angle / 2))) ** 1.22)

        H = Asteroid.abs_mag(self)

        return (H - 2.5 * math.log10((1 - self.G) * phi1 + self.G * phi2))
    


# pytest doesn't like asteroid import with abs_mag :( diameter isn' in phase functions but cannot process diameter from abs_mag 
# how do I add H as parameter to phase function?? AAAAAAAA