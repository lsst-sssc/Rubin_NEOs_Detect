import pytest

from neo_detect.asteroid import Asteroid

class Test_Abs_Mag:

    def test_diam_30m(self):
        expected_H = 25

        ast = Asteroid(30.0, albedo = 0.20)
        H = ast.abs_mag()

        assert H == pytest.approx(expected_H, abs=0.05)

    def test_diam_140m(self):
        expected_H = 22

        ast = Asteroid(140.0, 0.15)
        H = ast.abs_mag()

        assert H == pytest.approx(expected_H, abs=0.1)
    
