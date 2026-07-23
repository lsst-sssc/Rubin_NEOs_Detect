import pytest

from neo_detect.rubin_utils import calc_colors

class Test_Calc_Colors:
    def test_calc_colors_null(self):

        result = calc_colors()
        assert isinstance(result, dict)

    def test_calc_colors_S_type(self):
        sedname = 'S.dat'
        sed_dir = None
        result = calc_colors(sedname, sed_dir)
        assert isinstance(result, dict)
        assert 'V-u' in result
        assert 'V-g' in result
        assert 'V-r' in result
        assert 'V-i' in result
        assert 'V-z' in result
        assert 'V-y' in result
