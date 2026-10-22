"""Elevron Alt hardware masters: base panel, front axle stack, prop mount, fasteners and inserts."""
from robot.cad import fastener_catalog as fc
from .params_drive import WHEEL_GAP

# ---- MASTER DESIGN PARAMETERS ----------------------------------------------------------------------------------------
BASE_T = 1.0                          # printed base panel in the 2 mm rebate (Revron RV26 is 1 mm too)
SO_LEN, SO_D = 10.0, 5.0              # 10mm_standoff_3m_alu (STEP 10 x 5)
BACK_T, FRONT_T = 3.0, 1.9            # BACKING_PLATE / FRONT_PLATE thickness (STEP)
PLATE_W, PLATE_H = 10.0, 12.8         # BACKING_PLATE face (STEP 10 x 12.8); the FRONT_PLATE is PLATE_W square
PROP_D = 15.0                         # RV07 prop-mount flange
FH_CLR = 0.2                          # front hub bore round the standoff (running fit)
INSERT_CAT = "heatset_m2_4"           # M2 heat-sets in the 2.9 column bores (both ends)
M2, M3 = 2.0, 3.0
# -----------------------------------------------------------------------------------------------------------------------
BASE_CSK_D = fc.head(M2, "csk")[0]    # ISO M2 countersunk head diameter
FRONT_HUB_TRIM = FRONT_T + WHEEL_GAP  # the front hub's inner end is cut back to clear the FRONT_PLATE

__all__ = [n for n in dir() if not n.startswith("__")]
