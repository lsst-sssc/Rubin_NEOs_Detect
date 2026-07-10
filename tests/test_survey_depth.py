import pytest
import datetime

from neo_detect.asteroid import Asteroid
from neo_detect.survey_depth import Constant_Depth

class Test_Constant_Depth:
    def test_constant_depth(self):
        expected_depth = 24.52

        rubin_depth = Constant_Depth()

        assert rubin_depth.depth(datetime.datetime(2026, 7, 2)) == expected_depth

class Test_Fancier_Rubin_Depth:
    pass
