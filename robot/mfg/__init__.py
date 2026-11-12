"""Manufacturing pack: turn a built robot into what a builder needs (UNTESTED first cut).

pack.write(spec, out_dir) -> files: per-part STL/STEP in print/cut orientation, DXF flats, BOM + COTS buy list,
fastener counts, mass budget vs the class limit, print settings per part, sheet cut list, ordered assembly steps,
and one BUILD.md / BUILD.html guide. Pure-data helpers (bom, budget, printing, cutlist, steps) take a Spec and,
optionally, a resolved robot / world, so they can be unit-tested without a B-rep build.
"""

from .bom import bom, buy_list, fastener_counts  # noqa: F401
from .budget import mass_budget  # noqa: F401
from .printing import print_settings  # noqa: F401
from .cutlist import cut_list  # noqa: F401
from .steps import assembly_steps  # noqa: F401
