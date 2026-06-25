import pytest
import math

from neo_detect.phase_fnc import Phase_Function

class Test_Phase_Function:
    def test_angle_0(self):
        expected_phi = 1.0

        pf = Phase_Function(0.0, G=0.15)
        phi = pf.phase_function()

        assert phi == pytest.approx(expected_phi, abs=1e-6)

    def test_angle_90(self):
        expected_phi = 0.5

        pf = Phase_Function(90.0, G=0.15)
        phi = pf.phase_function()

        assert phi == pytest.approx(expected_phi, abs=1e-6)

    def test_angle_180(self):
        expected_phi = 0.0

        pf = Phase_Function(180.0, G=0.15)
        phi = pf.phase_function()

        assert phi == pytest.approx(expected_phi, abs=1e-6)