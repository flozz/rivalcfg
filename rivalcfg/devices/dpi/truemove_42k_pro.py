"""CPI Values for TrueMove 42K Pro sensor.

The DPI is sent as-is (no conversion). SteelSeries GG allows values from 1 to
65000 DPI (the sensor's native maximum is 42000 DPI).
"""

choices = {dpi: dpi for dpi in range(1, 65001)}
