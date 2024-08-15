import sys
from pathlib import Path
matcha_path = Path(__file__).parent
sys.path.append(str(matcha_path))

from .load import *
from .generation import *


cosy_voice_model = [
    "CosyVoice-300M-SFT",
]
