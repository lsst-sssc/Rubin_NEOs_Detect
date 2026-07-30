import sqlite3
import datetime
import pathlib

import pytest

from neo_detect.survey_depth import Constant_Depth, OpSim_Depth

# A small (~50 row) sample of real observations drawn from the Rubin
# baseline_v5.3.0_10yrs cadence, committed to the repo so that tests exercise a
# genuine OpSim schema without needing the full multi-hundred-MB database. This
# is what guards against schema drift (e.g. the band/filter column change) on
# real production files, and it runs in CI.
SAMPLE_OPSIM_DB = pathlib.Path(__file__).parent / "data" / "opsim_sample_v5.3.0_10yrs.db"
SAMPLE_OPSIM_ROWS = 50

class Test_Constant_Depth:
    def test_constant_depth(self):
        expected_depth = 24.52

        rubin_depth = Constant_Depth()

        assert rubin_depth.depth(datetime.datetime(2026, 7, 2)) == expected_depth


@pytest.fixture
def opsim_db(tmp_path):
    """A minimal OpSim-style sqlite3 database with an ``observations`` table.

    Includes columns beyond the ones OpSim_Depth reads, to verify that only
    the requested columns are selected.
    """
    db_path = tmp_path / "opsim_test.db"
    con = sqlite3.connect(db_path)
    con.execute(
        """
        CREATE TABLE observations (
            observationId INTEGER,
            observationStartMJD REAL,
            flush_by_mjd REAL,
            band TEXT,
            fiveSigmaDepth REAL,
            airmass REAL,
            skyBrightness REAL
        )
        """
    )
    rows = [
        (0, 61208.2013, 61208.2559, "u", 23.877, 1.038, 21.5),
        (1, 61208.2019, 61208.2559, "g", 24.512, 1.046, 21.9),
        (2, 61208.2024, 61208.2559, "r", 24.203, 1.056, 20.8),
    ]
    con.executemany(
        "INSERT INTO observations VALUES (?, ?, ?, ?, ?, ?, ?)", rows
    )
    con.commit()
    con.close()
    return db_path


class Test_OpSim_Depth_Real_Data:
    def test_reads_expected_columns(self):
        depth = OpSim_Depth(str(SAMPLE_OPSIM_DB))

        assert list(depth.observations.columns) == list(OpSim_Depth.COLUMNS)

    def test_reads_all_sampled_rows(self):
        depth = OpSim_Depth(str(SAMPLE_OPSIM_DB))

        assert len(depth.observations) == SAMPLE_OPSIM_ROWS

    def test_values_are_sane(self):
        obs = OpSim_Depth(str(SAMPLE_OPSIM_DB)).observations

        assert set(obs["band"].unique()).issubset({"u", "g", "r", "i", "z", "y"})
        assert obs["fiveSigmaDepth"].between(15.0, 27.0).all()
        assert (obs["airmass"] >= 1.0).all()
        assert (obs["observationStartMJD"] > 59000.0).all()


class Test_OpSim_Depth:
    def test_reads_expected_columns(self, opsim_db):
        depth = OpSim_Depth(str(opsim_db))

        assert list(depth.observations.columns) == list(OpSim_Depth.COLUMNS)

    def test_reads_all_rows(self, opsim_db):
        depth = OpSim_Depth(str(opsim_db))

        assert len(depth.observations) == 3

    def test_values_match(self, opsim_db):
        depth = OpSim_Depth(str(opsim_db))
        first = depth.observations.iloc[0]

        assert first["band"] == "u"
        assert first["fiveSigmaDepth"] == pytest.approx(23.877)
        assert first["airmass"] == pytest.approx(1.038)
        assert first["observationStartMJD"] == pytest.approx(61208.2013)

    def test_opens_read_only(self, opsim_db):
        depth = OpSim_Depth(str(opsim_db))

        with pytest.raises(sqlite3.OperationalError):
            con = sqlite3.connect(f"file:{depth.db_path}?mode=ro", uri=True)
            try:
                con.execute("DELETE FROM observations")
            finally:
                con.close()

    def test_depth_returns_nearest_visit(self, opsim_db):
        depth = OpSim_Depth(str(opsim_db))

        # Star date 2026-09-01 is MJD 61208.0, which is very close to the first three rows in the test DB
        date = datetime.datetime(2026, 9, 1, tzinfo=datetime.timezone.utc)
        band = "g"
        expected_depth = 24.512