"""Model class, to be extended by specific types of models."""
from pathlib import Path 
from typing import Callable, Dict
from torchsummary import summary

from fastai.vision import DataBunch, Learner, error_rate
from torch.nn import Module

from squat_recognizer.datasets.dataset_bunch import DatasetBunch

DIRNAME = Path(__file__).parents[1].resolve() / "weights"
EXPORT_DIRNAME = Path(__file__).parents[1].resolve() / "exports"

class Model:
  """Base class, to be subclassed by predictors for specific type of data."""
  def __init__(
    self,
    dataset_cls: type,
    learner_fn: Callable[..., Learner],
    network_fn: Callable[..., Module],
    dataset_args: Dict = None):

    self.network_fn = network_fn
    self.learner_fn = learner_fn

    self.name = f"{self.__class__.__name__}_{dataset_cls.__name__}_{network_fn.__name__}"

    if dataset_args is None:
      dataset_args = {}
    self.dataset = dataset_cls(**dataset_args)

  @property
  def image_shape(self):
    return self.dataset.input_shape

  def weights_filename(self, stage: str) -> str:
    DIRNAME.mkdir(parents=True, exist_ok=True)
    return str(DIRNAME / f"{self.name}_weights_{stage}")

  @property
  def export_filename(self) -> str:
    ## EXPORT_DIRNAME.mkdir(parents=True, exist_ok=True)
    ## return EXPORT_DIRNAME / f"{self.name}.pkl"
    return f"{self.name}.pkl"

  def fit(self, databunch: DataBunch, stage_one: Dict, stage_two: Dict = None, save_weights: bool = False) -> Learner:
    """
    Fits a learner to the databunch given the training specs, 
    and returns the learner.
    """
    learner = self.learner_fn(databunch, self.network_fn, metrics=error_rate)

    # Stage one of training.
    s1_epochs = stage_one["epochs"]
    s1_one_cycle = stage_one["one_cycle"]

    if s1_one_cycle == 1:
      learner.fit_one_cycle(s1_epochs)
    else:
      learner.fit(s1_epochs)

    if save_weights:
      self.save_weights(learner, 'stage-1')

    if stage_two is None:
      return

    # Stage two of training.
    s2_unfreeze = stage_two["unfreeze"]
    s2_epochs = stage_two["epochs"]
    s2_one_cycle = stage_two["one_cycle"]
    s2_max_lr_start = float(stage_two["max_lr_start"])
    s2_max_lr_end = float(stage_two["max_lr_end"])

    lr_slice = slice(s2_max_lr_start, s2_max_lr_end)


    if s2_unfreeze == 1:
      learner.unfreeze()

    if s2_one_cycle == 1:
      learner.fit_one_cycle(s2_epochs, max_lr=lr_slice)
    else:
      learner.fit(s2_epochs, max_lr=lr_slice)

    if save_weights:
      self.save_weights(learner, 'stage-2')
    
    return Learner
  
  def save_weights(self, learner: Learner, stage: str):
    learner.save(self.weights_filename(stage))
  
  def load_weights(self, learner: Learner, stage: str):
    learner.load(self.weights_filename(stage))
    return learner

  def export(self, learner: Learner):
    learner.export(self.export_filename)

  ## def __repr__(self):
  ##   return summary(self.learner.model)
    
  