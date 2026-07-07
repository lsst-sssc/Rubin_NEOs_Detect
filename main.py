from datetime import datetime

import numpy as np

from neo_detect.asteroid import Asteroid
from neo_detect.survey_depth import Constant_Depth

def compute_candle_flame(diameter=30.0, albedo=0.14, G=0.15, depth_model=None):
    """Return a Cartesian grid + boolean mask of where mag <= mag_lim.
    """

    if depth_model is None:
        depth_model = Constant_Depth()

    # Create an asteroid object
    asteroid = Asteroid(diameter=diameter, albedo=albedo, G=G)

    # Compute the absolute magnitude H from diameter and albedo
    H = asteroid.abs_mag()

    # Get the limiting magnitude from the depth model
    mag_lim = depth_model.depth(datetime.now())

    # Create Cartesian grid here
    x, y = None, None  # Placeholder for grid creation logic
    ### x, y = asteroid.cartesian_grid()

    # Convert Cartesian grid to distance and phase angle here
    ### r, delta, phase_angle = asteroid.cartesian_grid(x, y)

    # Compute apparent magnitude for each point in the grid
    mag = np.full_like(x, np.nan)
    ### mag = asteroid.apparent_magnitude(r, delta, phase_angle)


    # Future refinement: Calculate elongation angle and filter out points with elongation < 30 degrees
    # Hint: use dot product to compute elongation angle between Sun and asteroid as seen from Earth

    # Create a boolean mask of where the apparent magnitude is less than or equal to the limiting magnitude
    # Later: add in mask from elongation angle filter
    detectable_mask = mag <= mag_lim

    return {
        "H": H,
        "mag_lim": mag_lim,
        "x": x,
        "y": y,
        "mag": mag,
        "detectable_mask": detectable_mask
    }

def plot_candle_flame(results, diameter, albedo):
    pass


if __name__ == "__main__":

    diameter = 30.0 # meters
    albedo = 0.14
    G = 0.15

    depth = Constant_Depth()
    results = compute_candle_flame(diameter, albedo, G, depth_model=depth)

    print(f"Asteroid: D = {diameter:.0f} m, p_V = {albedo:.2f}  ->  H = {results['H']:.2f}")
    print(f"Limiting magnitude: m_lim = {results['mag_lim']:.2f}")

    # Plot results (we pass in diameter and albedo for caption purposes)
    plot_candle_flame(results, diameter, albedo)
