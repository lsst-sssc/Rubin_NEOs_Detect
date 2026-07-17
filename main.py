from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

from neo_detect.asteroid import Asteroid
from neo_detect.survey_depth import Constant_Depth

def compute_candle_flame(diameter=30.0, albedo=0.14, G=0.15, depth_model=None, n_grid_pts=1200):
    """Return a Cartesian grid + boolean mask of where mag <= mag_lim.
    """

    # Distance from observer to Sun in AU (assumed to be 1 AU)
    r_obs = 1.0  # AU

    if depth_model is None:
        depth_model = Constant_Depth()

    # Create an asteroid object
    asteroid = Asteroid(diameter=diameter, albedo=albedo, G=G)
    # Compute the absolute magnitude H from diameter and albedo
    H = asteroid.abs_mag()

    # Get the limiting magnitude from the depth model
    mag_lim = depth_model.depth(datetime.now())

    # Create Cartesian grid here centred on the observer, with Sun-observer axis = x.
    x = np.linspace(r_obs - 2.0, r_obs + 2.0, n_grid_pts)
    y = np.linspace(-1.0, 1.0, n_grid_pts)
    x, y = np.meshgrid(x, y)

    # Convert Cartesian grid to distance and phase angle here
    r, delta, phase_angle = asteroid.cartesian_grid(x, y)

    # Remove invalid points inside the Sun or Earth
    valid = (r > 1e-4) & (delta > 1e-4)

    # Compute apparent magnitude for each point in the grid
    mag = np.full_like(x, np.nan)
    mag[valid] = asteroid.apparent_magnitude(r[valid], delta[valid], phase_angle[valid])

    # Create a boolean mask of where the apparent magnitude is less than or equal to the limiting magnitude
    brightness_mask = boolean_mask(mag, mag_lim)

    # TL: Add call to elongation_angle function here, and filter out points with 
    # elongation < 30 degrees. Return a boolean mask of where elongation >= 30 degrees. 
    # Then combine this mask with the detectable_mask to get the final mask of detectable 
    # points.
    sun_vector = np.array([-r_obs, 0.0, 0.0])  # observer-> sun vector
    asteroid_vector = np.array([x - r_obs, y, np.zeros_like(x)])  # observer-> asteroid vector
    earth_vector = np.array([0.0, 0.0, 0.0])  # observer-> earth vector (at origin)

    elongation = elongation_angle(sun_vector, asteroid_vector, earth_vector)
    # Create a boolean mask of where the elongation angle is greater than or equal to 30 degrees
    observable_mask = elongation >= 30.0

    # Combine masks to get the final detectable mask
    detectable_mask = valid & brightness_mask & observable_mask

    # Return results as a dictionary
    return {
        "H": H,
        "mag_lim": mag_lim,
        "x": x,
        "y": y,
        "mag": mag,
        "detectable_mask": detectable_mask,
        }

def boolean_mask(mag, mag_lim):
    """Returns a boolean mask of where the apparent magnitude is less than or equal to the limiting magnitude
    """
    return mag <= mag_lim

def elongation_angle(sun_vector, asteroid_vector, earth_vector):
    """Computes the elongation angle between the Sun and an asteroid as seen from Earth using a shared coordinate system.
    """
    # Reference: https://community.lsst.org/t/dp0-3-lacks-solar-elongation-angle-data/9355/5 (Hopefully this is correct)

    # Compute the relative vectors from Earth to Sun and Earth to Asteroid
    sun_from_earth = sun_vector # - earth_vector
    asteroid_from_earth = asteroid_vector # - earth_vector

    # Compute the dot product
#    dot_product = np.dot(sun_from_earth, asteroid_from_earth)
    dot_product = sun_from_earth[0] * asteroid_from_earth[0] + sun_from_earth[1] * asteroid_from_earth[1] + sun_from_earth[2] * asteroid_from_earth[2]
    sun_magnitude = np.hypot(sun_from_earth[0], sun_from_earth[1])
    asteroid_magnitude = np.hypot(asteroid_from_earth[0], asteroid_from_earth[1], asteroid_from_earth[2])
    # Compute the magnitudes of both relative vectors
#    sun_magnitude = np.linalg.norm(sun_from_earth)
#    asteroid_magnitude = np.linalg.norm(asteroid_from_earth)

    # Compute and clamp the cosine value
    cos_angle = dot_product / (sun_magnitude * asteroid_magnitude)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    # Return the angle in degrees
    return np.degrees(np.arccos(cos_angle))

def plot_candle_flame(results, diameter, albedo, savepath=None):
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