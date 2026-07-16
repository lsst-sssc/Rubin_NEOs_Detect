import pytest
import numpy as np

from main import compute_candle_flame

class Test_ComputeCandleFlame:
    def test_compute_candle_flame(self):
        # Test with known values
        diameter = 100  # meters
        albedo = 0.15
        mag_lim = 24.5

        results = compute_candle_flame(diameter, albedo, mag_lim)

        # Check that the results contain expected keys
        assert "H" in results
        assert "mag_lim" in results
        assert "x" in results
        assert "y" in results
        assert "mag" in results
        assert "detectable_mask" in results

        # Check that the detectable mask is a boolean array of the same shape as x and y
        assert isinstance(results["detectable_mask"], np.ndarray)
        assert results["detectable_mask"].dtype == bool
        assert results["detectable_mask"].shape == results["x"].shape
