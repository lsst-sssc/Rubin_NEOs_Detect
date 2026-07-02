import ast
import numpy as np
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
    
    def test_cartesian_grid_x1y1(self):
        x = 1.0
        y = 1.0
        expected_r, expected_delta, expected_phase_angle = 1.414, 1.0, 45.0 

        ast = Asteroid(diameter = 3.6, albedo = 0.14, G = 0.15)
        r_2d, delta_2d, phase_angle_2d = ast.cartesian_grid(x, y)
        

        assert r_2d == pytest.approx(expected_r, abs = 1e-3)
        assert delta_2d == pytest.approx(expected_delta, abs = 1e-3)
        assert phase_angle_2d == pytest.approx(expected_phase_angle, abs = 0.1)


    def test_cartesian_grid_x0y1(self):
        x = 0.0
        y = -1.0
        expected_r, expected_delta, expected_phase_angle = 1.0, 1.414, 45.0 

        ast = Asteroid(diameter = 3.6, albedo = 0.14, G = 0.15)
        r_2d, delta_2d, phase_angle_2d = ast.cartesian_grid(x, y)
        

        assert r_2d == pytest.approx(expected_r, abs = 1e-3)
        assert delta_2d == pytest.approx(expected_delta, abs = 1e-3)
        assert phase_angle_2d == pytest.approx(expected_phase_angle, abs = 0.1)


    def test_cartesian_grid_x05y05(self):
        x = 0.5
        y = 0.5
        expected_r, expected_delta, expected_phase_angle = 0.707, 0.707, 90.0 

        ast = Asteroid(diameter = 3.6, albedo = 0.14, G = 0.15)
        r_2d, delta_2d, phase_angle_2d = ast.cartesian_grid(x, y)
        

        assert r_2d == pytest.approx(expected_r, abs = 1e-3)
        assert delta_2d == pytest.approx(expected_delta, abs = 1e-3)
        assert phase_angle_2d == pytest.approx(expected_phase_angle, abs = 0.1)

    def test_cartesian_grid_x06y04(self):
        x = 0.6
        y = 0.4
        expected_r, expected_delta, expected_phase_angle = 0.721, 0.566, 101.0 

        ast = Asteroid(diameter = 3.6, albedo = 0.14, G = 0.15)
        r_2d, delta_2d, phase_angle_2d = ast.cartesian_grid(x, y)
        

        assert r_2d == pytest.approx(expected_r, abs = 1e-3)
        assert delta_2d == pytest.approx(expected_delta, abs = 1e-3)
        assert phase_angle_2d == pytest.approx(expected_phase_angle, abs = 1.0)


    def test_cartesian_grid_x2y05(self):
        x = 2.0
        y = -0.5
        expected_r, expected_delta, expected_phase_angle = 2.061, 1.118, 12.0

        ast = Asteroid(diameter = 3.6, albedo = 0.14, G = 0.15)
        r_2d, delta_2d, phase_angle_2d = ast.cartesian_grid(x, y)
        

        assert r_2d == pytest.approx(expected_r, abs = 1e-3)
        assert delta_2d == pytest.approx(expected_delta, abs = 1e-3)
        assert phase_angle_2d == pytest.approx(expected_phase_angle, abs = 1.0)

    def test_cartesian_grid_array(self):
        x = np.array([2.0])
        y = np.array([-0.5])
        expected_r, expected_delta, expected_phase_angle = 2.061, 1.118, 12.0

        ast = Asteroid(diameter = 3.6, albedo = 0.14, G = 0.15)
        r_2d, delta_2d, phase_angle_2d = ast.cartesian_grid(x, y)
        

        assert r_2d == pytest.approx(expected_r, abs = 1e-3)
        assert delta_2d == pytest.approx(expected_delta, abs = 1e-3)
        assert phase_angle_2d == pytest.approx(expected_phase_angle, abs = 1.0)


    def test_app_mag_date(self): 
        expected_m = 32.444
        date = '2026-07-02'
        diameter = 3.6

        ast = Asteroid(diameter=diameter, albedo=0.14, G=0.15)
        m = ast.apparent_magnitude_date(date)

        assert m == pytest.approx(expected_m, abs = 0.1)


    
        