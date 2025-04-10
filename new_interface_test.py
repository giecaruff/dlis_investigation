import numpy as np
from dlisio_r import DLISAccess

#info = DLISAccess(r"C:\Users\mario\Documents\GitHub\stoneforge\stoneforge\datasets\DSDP_leg_96_hole_616_96_original_data.dlis")
info = DLISAccess(r"D:\santos_from_bruna\1-BRSA-369A-RJS\Perfis\DLIS\Original\1-brsa-369a-rjs__msct3_8.dlis")
print(info.get_data())