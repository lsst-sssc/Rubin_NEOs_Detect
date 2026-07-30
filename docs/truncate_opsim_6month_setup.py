# coding: utf-8
import os
import time
from pathlib import  Path
from datetime import datetime, timedelta

from astropy.time import Time

from neo_detect.survey_depth import OpSim_Depth
from neo_detect.rubin_utils import truncate_opsim


db_path = Path(os.environ['RUBIN_SIM_DATA_DIR']) / 'sim_baseline' / 'baseline.db'

start_date = datetime(2026, 9, 1)
end_date = start_date + timedelta(days=181)
print(f"Opsim span: {start_date} -> {end_date}")

new_db_path, opsim = truncate_opsim(start_date, end_date, db_path)
new_db_path, len(opsim)
start = time.time()
depth = OpSim_Depth(db_path)
end = time.time()
print(f"Read took {end-start:.1f}s")


start = time.time()
depth = OpSim_Depth(new_db_path)
end = time.time()
print(f"Read took {end-start:.1f}s")
