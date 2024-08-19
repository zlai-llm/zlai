import sys
from pathlib import Path
matcha_path = Path(__file__).parent
sys.path.insert(0, str(matcha_path))

from .generation import *


cosy_voice_model = [
    "CosyVoice-300M-SFT",
]
