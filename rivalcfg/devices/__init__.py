from . import rival100


def get_profile(vendor_id=0x1038, product_id=None):
    # FIXME just return a profile to allow to develop the rest of the software
    for k, v in rival100.profile["models"][0].items():
        rival100.profile[k] = v
    return rival100.profile
