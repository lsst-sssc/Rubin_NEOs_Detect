import pytest 

from neo_detect.app_mag import Apparent_Magnitude

class Test_Apparent_Magnitude:
    def test_app_mag_15H_angle0(self):
        expected_m = 15

        app_mag = Apparent_Magnitude(H = 15.0, G = 0.15)
        m = app_mag.apparent_magnitude(r = 1.0, delta = 1.0, phase_angle = 0.0)

        assert m == pytest.approx(expected_m, abs = 0.1)

    def test_app_mag_15H_angle30(self):
        expected_m = 15.7

        app_mag = Apparent_Magnitude(H = 15.0, G = 0.15)
        m = app_mag.apparent_magnitude(r = 1.0, delta = 1.0, phase_angle = 30.0)

        assert m == pytest.approx(expected_m, abs = 0.1)


    def test_app_mag_30H_angle30(self):
        expected_m = 30.7

        app_mag = Apparent_Magnitude(H = 30.0, G = 0.15)
        m = app_mag.apparent_magnitude(r = 1.0, delta = 1.0, phase_angle = 30.0)

        assert m == pytest.approx(expected_m, abs = 0.1)