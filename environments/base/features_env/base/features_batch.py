from dataclasses import dataclass
from torch import Tensor
from typing import Optional

@dataclass
class FeatureBatch:
    features: Tensor
    mask: Optional[Tensor] = None
