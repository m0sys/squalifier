"""DatasetBunch class."""
from typing import Optional, Tuple
from fastai.vision import LabelLists, get_transforms, TfmList, imagenet_stats


class DatasetBunch:
    """This is a databunch that is not being used anywhere yet"""

    def __init__(
        self,
        src: LabelLists,
        size: int,
        bs: int = 64,
        transform: Optional[Tuple[TfmList, TfmList]] = get_transforms(),
        normalization_stats=imagenet_stats,
    ):
        self.data = src.transform(transform, size=size).databunch(bs=bs).normalize(normalization_stats)
