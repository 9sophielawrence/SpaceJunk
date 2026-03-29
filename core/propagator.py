from sgp4.api import Satrec, jday
from datetime import datetime, timedelta
import numpy as np

class Propagator:
    def __init__(self, tle_line1: str, tle_line2: str):
        self.sat = Satrec.twoline2rv(tle_line1, tle_line2)
        self.norad_id = int(tle_line1[2:7])

    def position_at(self, dt: datetime) -> np.ndarray:
        """Returns ECI position in km"""
        jd, fr = jday(dt.year, dt.month, dt.day,
                      dt.hour, dt.minute, dt.second + dt.microsecond/1e6)
        e, r, v = self.sat.sgp4(jd, fr)
        if e != 0:
            raise ValueError(f"SGP4 error code {e} for NORAD {self.norad_id}")
        return np.array(r)

    def propagate_window(self, start: datetime, hours: float,
                         step_seconds: int = 60) -> list:
        steps = int(hours * 3600 / step_seconds)
        results = []
        for i in range(steps):
            dt = start + timedelta(seconds=i * step_seconds)
            try:
                pos = self.position_at(dt)
                results.append((dt, pos))
            except ValueError:
                continue
        return results
    