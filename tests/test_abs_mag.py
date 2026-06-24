import pytest
from neo_detect.abs_mag import abs_mag

class Test_Abs_Mag:

    def test_diam_30m(self):
        expected_H = 42

        H = abs_mag(30.0, albedo = 0.14)
        
        assert H == expected_H
    def test_diam_140m(self):
        expected_H = 22

        H = abs_mag(140.0, albedo = 0.15)
        
        assert H == expected_H