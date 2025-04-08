import numpy as np
from dlisio import dlis
import pandas as pd
from dlisio_r import DLISAccess

info = DLISAccess(r"C:\Users\mario\Documents\GitHub\stoneforge\stoneforge\datasets\DSDP_leg_96_hole_616_96_original_data.dlis")
info.preview()