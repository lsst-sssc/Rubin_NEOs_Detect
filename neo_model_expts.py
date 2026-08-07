from pathlib import Path

from rubin_scheduler.data import get_data_dir

from neo_detect.neo_model import NEOMOD3, Granvik

if __name__ == "__main__":
    data_root = Path(get_data_dir()) / "orbits"
    neomod3 = NEOMOD3(data_root=data_root, filename='neomod3_5k_diam_0.01-1.0.txt')
    neomod3.load_table(neomod3.path)

    print(f"NEOMOD3 table loaded with {len(neomod3.neo_table)} rows and columns: {neomod3.neo_table.colnames}")

    granvik = Granvik(data_root=data_root, filename='granvik_5k.txt')
    granvik.load_table(granvik.path)

    print(f"Granvik table loaded with {len(granvik.neo_table)} rows and columns: {granvik.neo_table.colnames}")

    # Make plots
    neomod3.plot_H()
    granvik.plot_H()