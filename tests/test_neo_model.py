import pathlib
import shutil

from neo_detect.neo_model import NEOMOD3, Granvik

SAMPLE_NEOMOD3 = pathlib.Path(__file__).parent / "data" / "neomod3_sample.txt"
SAMPLE_GRANVIK = pathlib.Path(__file__).parent / "data" / "granvik_5k_sample.txt"
SAMPLE_GRANVIK_PHA = pathlib.Path(__file__).parent / "data" / "granvik_pha_5k_sample.txt"

class Test_NEOMOD3:
    def test_load_table(self, tmp_path):
        # Copy the sample file to a temporary location for testing
        test_file = tmp_path / "neomod3_sample.txt"
        shutil.copy(SAMPLE_NEOMOD3, test_file)

        # Create an instance of NEOMOD3 with the temporary file
        neomod3 = NEOMOD3(data_root=tmp_path, filename="neomod3_sample.txt")

        # Load the table and check its contents
        table = neomod3.neo_table

        # Check that the table has the expected columns
        expected_columns = ["H", "a", "e", "inc", "diam", "pV"]
        assert all(col in table.colnames for col in expected_columns)

        # Check that the table has the expected number of rows (based on the sample)
        assert len(table) == 10


class Test_Granvik:
    def test_load_granvik_table(self, tmp_path):
        test_file = tmp_path / "granvik_5k_sample.txt"
        shutil.copy(SAMPLE_GRANVIK, test_file)

        granvik = Granvik(data_root=tmp_path, filename="granvik_5k_sample.txt")
        table = granvik.neo_table

        expected_columns = ["a", "e", "inc", "Omega", "argPeri", "meanAnomaly", "epoch", "H", "MOID", "objId", "g", "sed_filename"]
        assert all(col in table.colnames for col in expected_columns)
        assert len(table) == 10

    def test_load_granvik_pha_table(self, tmp_path):
        test_file = tmp_path / "granvik_pha_5k_sample.txt"
        shutil.copy(SAMPLE_GRANVIK_PHA, test_file)

        granvik = Granvik(data_root=tmp_path, filename="granvik_pha_5k_sample.txt")
        table = granvik.neo_table

        expected_columns = ["a", "e", "inc", "Omega", "argPeri", "meanAnomaly", "epoch", "H", "MOID", "objId", "g", "sed_filename"]
        assert all(col in table.colnames for col in expected_columns)
        assert len(table) == 10
