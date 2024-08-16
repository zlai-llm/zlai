from .flux import *
from .kolors import *

__all__ = ["load_method_mapping"]


load_method_mapping = {
    "load_kolors_diffusers": load_kolors_diffusers,
    "load_kolors_image2image": load_kolors_image2image,
    "load_flux_diffusers": load_flux_diffusers,
}
