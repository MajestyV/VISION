# This package is designed for visualizing scientific data specific for the field of electronic engineering.

from .TektronixFileConverter import convert

# Source code files of the package: KEITHLEY4200
# import KEITHLEY4200 as KEITHLEY4200  # Package handling data from KEITHLEY4200 semiconductor parameter analyzer
# from .KEITHLEY4200 import KEITHLEY4200  # Package handling data from KEITHLEY4200 semiconductor parameter analyzer
from . import KEITHLEY4200 as KEITHLEY4200  # Package handling data from KEITHLEY4200 semiconductor parameter analyzer