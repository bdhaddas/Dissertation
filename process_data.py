from A_CLEAN_DATA import clean_data_v2                 # quads                   -> XX in DATA
from B_MERGE_YEAR_PER_SITE import merge_year_per_site  # '' and XX in DATA       -> site_x_xxxx in DATA_OUT
from C_CALC import calc_v_3                            # site_x_xxxx in DATA_OUT -> site_x_xxxx-xxxx in DATA_CALC and DATA_CALC2
from C_CALC import vols_v3                             # site_x_xxxx-xxxx in DATA_CALC and DATA_CALC2 -> vols1.csv in DATA_CALC_VOLS and DATA_CALC2_VOLS
from C_CALC import vols_siteperyear                    # site_x_xxxx in DATA_OUT -> vols_siteperyear.csv in DATA_CALC_VOLS
from C_CALC import vols_change_siteperyear             # site_x_xxxx in DATA_OUT -> vols_change_siteperyear.csv in DATA_CALC_VOLS
