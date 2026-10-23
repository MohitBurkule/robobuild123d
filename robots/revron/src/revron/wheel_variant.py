"""Rear wheel setting: REVRON_REAR_WHEEL = a COTS wheel id (robot/catalog_data) sizes the rear tyre and sets the rear axle height from it;
unset / "stock" is the original RVRN 2.0 tyre (21.5 x 9.5). Read at import, then regenerate the spec (settings hook `wheel.rear`)."""
import os

REAR_WHEEL = os.environ.get("REVRON_REAR_WHEEL", "stock")
STOCK = dict(od=21.5, w=9.5)


def rear_wheel_dims():
    """{od, w} of the rear wheel (mm): the stock tyre, or the chosen catalogue wheel's diameter and width."""
    if REAR_WHEEL == "stock":
        return dict(STOCK)
    from robot import catalog
    props = catalog.find(REAR_WHEEL).props
    return dict(od=props["diameter_mm"], w=props["width_mm"])
