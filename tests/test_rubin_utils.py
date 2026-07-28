import pytest

from neo_detect.rubin_utils import calc_colors, transform_Vmag, RubinDetection

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

    'C.dat': {
        'V-u': -1.5080,
        'V-g': -0.2931,
        'V-r':  0.1761,
        'V-i':  0.2927,
        'V-z':  0.2980,
        'V-y':  0.3026,
    },

    'D.dat': {
        'V-u': -1.6287,
        'V-g': -0.3380,
        'V-r':  0.2311,
        'V-i':  0.4470,
        'V-z':  0.5320,
        'V-y':  0.6243,
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

    def test_calc_colors_C_type(self):
        sedname = 'C.dat'
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
    

    def test_calc_colors_D_type(self):
        sedname = 'D.dat'
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

    def test_calc_colors_invalid_sed(self):
        sedname = 'invalid_sed.dat'
        sed_dir = None
        with pytest.raises(FileNotFoundError):
            calc_colors(sedname, sed_dir)


@pytest.mark.parametrize(
    "sed_type, sed_file",
    [("s", "S.dat"), ("c", "C.dat"), ("d", "D.dat")],
)
@pytest.mark.parametrize("band", ["u", "g", "r", "i", "z", "y"])
def test_transform_Vmag_matches_expected_color_and_sed_type(sed_type, sed_file, band):
    vmag = 18.0
    color_key = f"V-{band}"

    # Check the shorthand SED type resolves to the expected file name
    resolved_sed = RubinDetection.SED_FILES.get(sed_type, sed_type)
    assert resolved_sed == sed_file

    # Get the expected color from calc_colors()
    color_data = calc_colors(sedname=sed_file, sed_dir=None)[sed_file]
    expected_color = EXPECTED_COLORS[sed_file][color_key]

    assert color_data[color_key] == pytest.approx(expected_color, abs=0.01)

    # Transform V mag -> Rubin mag and ensure it matches the expected relation
    transformed_mag = transform_Vmag(
        vmag,
        sed_type=sed_type,
        filter_name=band,
        filter_dir=None,
        sed_dir=None,
    )

    expected_mag = vmag - expected_color
    assert transformed_mag == pytest.approx(expected_mag, abs=0.01)