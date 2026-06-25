import math

class Phase_Function:
    def __init__(self, angle: float, G: float = 0.15):
        self.angle = angle
        self.G = G
        
    def phase_function(self):
        phi1 = math.exp(-3.33 * (math.tan(math.radians(self.angle / 2))) ** 0.63)
        phi2 = math.exp(-1.87 * (math.tan(math.radians(self.angle / 2))) ** 1.22)

        return (1 - self.G) * phi1 + self.G * phi2
        