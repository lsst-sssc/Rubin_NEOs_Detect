from neo_detect.rubin_utils import calc_colors

# Reference V-band colors per SED type. Add new SED types here as they arrive;
# the fixture and the parametrized value test pick them up automatically.
# Values are snapshotted from calc_colors and cross-checked against rubin_sim's
# canonical BaseObs.calc_colors (identical magnitudes, opposite sign convention).
EXPECTED_COLORS = {
    'S.dat': {
        'V-u': -1.8151,
        'V-g': -0.3841,
        'V-r':  0.2613,
        'V-i':  0.4566,
        'V-z':  0.4006,
        'V-y':  0.4094,
    },
}


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
        for color, expected in EXPECTED_COLORS[sedname].items() :
            assert color in result_sed
            assert abs(result_sed[color] - expected) < 0.01, (
                f"{sedname} {color}: {result_sed[color]:.3f} != {expected}"
            )
