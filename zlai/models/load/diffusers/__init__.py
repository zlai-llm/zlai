from .kolors import *
from .flux import *


load_method_mapping = {
    "load_kolors_diffusers": load_kolors_diffusers,
    "load_kolors_image2image": load_kolors_image2image,
    "load_flux_diffusers": load_flux_diffusers,
}
