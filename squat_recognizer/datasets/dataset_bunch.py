"""DatasetBunch class."""
from  fastai.vision import LabelLists, get_transforms, TfmList, imagenet_stats
from typing import Optional, Tuple

class DatasetBunch:

  def __init__(self, src: LabelLists, size: int, bs: int = 64, 
               transform: Optional[Tuple[TfmList, TfmList]] = get_transforms(), normalization_stats = imagenet_stats):
               self.data = (src.transform(transform, size=size)
                            .databunch(bs=bs).normalize(normalization_stats))