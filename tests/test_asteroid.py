import pytest
import math

from neo_detect.asteroid import Asteroid

class Test_Asteroid:

    def test_diam_30m(self):
        expected_H = 25

        ast = Asteroid(30.0, albedo = 0.20)
        H = ast.abs_mag()

        assert H == pytest.approx(expected_H, abs = 0.05)

    def test_diam_140m(self):
        expected_H = 22

        ast = Asteroid(140.0, albedo = 0.15)
        H = ast.abs_mag()

        assert H == pytest.approx(expected_H, abs = 0.1)

    def test_angle_0(self):
        expected_phi = 1.0

        ast = Asteroid(30, albedo = 0.14, G = 0.15)
        phi = ast.phase_function(0.0)

        assert phi == pytest.approx(expected_phi, abs=1e-3)

    def test_angle_90(self):
        expected_phi = 0.0535

        ast = Asteroid(30, 0.14, G = 0.15)
        phi = ast.phase_function(90.0)

        assert phi == pytest.approx(expected_phi, abs=1e-3)

    def test_angle_180(self):
        expected_phi = 0.0

        ast = Asteroid(30, 0.14, G = 0.15)
        phi = ast.phase_function(180.0)

        assert phi == pytest.approx(expected_phi, abs=1e-3)

    def test_app_mag_15H_angle0(self):
        expected_m = 15

        ast = Asteroid(diameter=3600, albedo=0.14, G=0.15)
        m = ast.apparent_magnitude(r = 1.0, delta = 1.0, phase_angle = 0.0)

        assert m == pytest.approx(expected_m, abs = 0.1)

    def test_app_mag_15H_angle30(self):
        expected_m = 16.3

        ast = Asteroid(diameter=3600, albedo=0.14, G=0.15)
        m = ast.apparent_magnitude(r = 1.0, delta = 1.0, phase_angle = 30.0)

        assert m == pytest.approx(expected_m, abs = 0.1)


    def test_app_mag_30H_angle30(self):
        expected_m = 31.3

        ast = Asteroid(diameter=3.6, albedo=0.14, G=0.15)
        m = ast.apparent_magnitude(r = 1.0, delta = 1.0, phase_angle = 30.0)

        assert m == pytest.approx(expected_m, abs = 0.1)
    
    def test_cartesian_grid(self): 
        ast = Asteroid(diameter = 3600, albedo = 0.14, G = 0.15)
        
        x_coords = [-1, 0.0, 1.0]
        y_coords = [-1, 0.0, 1.0]
        
        for x in x_coords:
            for y in y_coords:
                r = math.sqrt(x**2 + y**2)
                delta = math.sqrt((x - 1)**2 + (y - 1)**2)
                phase_angle = math(#???)
                
                m = ast.apparent_magnitude(r = r, delta = delta, phase_angle = phase_angle)
            
                assert m > 10 and m < 40
