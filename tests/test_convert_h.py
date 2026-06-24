from unicodedata import name

import pytest
import math

class Test_Convert_H:
    def __init__(self, diameter: float , albedo: float = 0.14):
        self.diameter = diameter
        self.albedo = albedo

    def H(self):
        expected_H = 25
        H = 15.618 - 5 * math.log10(self.diameter) - 2.5 * math.log10(self.albedo)
        return H 

if name == "__main__":
    Asteroid = Test_Convert_H(30.0, 0.14)
    print(Asteroid.H())