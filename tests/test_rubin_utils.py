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
        assert sedname in result
        result_sed = result[sedname]
        assert 'V-u' in result_sed
        assert 'V-g' in result_sed
        assert 'V-r' in result_sed
        assert 'V-i' in result_sed
        assert 'V-z' in result_sed
        assert 'V-y' in result_sed

    def filter_test(self):
        expected_colors = {
            'V-g': -0.254,
            'V-r': 0.213,
            'V-i': 0.356,
            'V-z': 0.322,
            'V-y': 0.314
        }
        assert all(abs(calc_colors()['S.dat'][color] - expected_colors[color]) < 0.01 for color in expected_colors)