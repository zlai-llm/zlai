from .flux import *
from .kolors import *


__all__ = [
    "diffusers_mapping"
]

flux_models = [
    "FLUX.1-dev"
]
flux_mapping = dict.fromkeys(flux_models, flux_generation)

diffusers_mapping = {
    **flux_mapping,
    **{"Kolors-diffusers": kolors_generation},
    **{"Kolors-image2image": kolors_img2img_generation},
}
