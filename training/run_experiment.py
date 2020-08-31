"""Script to run an experiment."""
import argparse
import json
import importlib
from typing import Dict
import os
import warnings

from training.training_utils import train_model

warnings.filterwarnings("ignore")


DEFAULT_TRAIN_ARGS = {
    "batch_size": 64,
    "stage_one": {"one_cycle": 1, "epochs": 4},
    "stage_two": {"unfreeze": 1, "one_cycle": 1, "max_lr_start": 3e-5, "max_lr_end": 3e-4, "epochs": 2},
}


def run_experiment(experiment_config: Dict, save_weights: bool, export: bool, gpu_ind: int):
    """
  Run a training experiment.

  Parameters
  ----------
  experiment_config (dict)
    of the form
    {
      "dataset": "FvbsDataset"
      "dataset_args": {
        "image_size": 224,
        "subsample_fraction": 0.2
      },
      "model": "CnnClassificationModel",
      "network": "resnet34",
      "learner_args": {
        ...
      },
      "train_args": {
        "batch_size": 64,
        "stage_one": {
          "one_cycle": 1,
          "epochs": 10,
        },
        "stage_two": {
          "unfreeze": 1,
          "one_cycle": 1,
          "max_lr_start": 3e-4,
          "max_lr_end": 3e-3
          "epochs": 15
        }
      }
    }

  save_weights (bool)
    If True, we will save the final model weights to a canoncial location.
    (see Model in models/base.py)
  gpu_ind (int)
    Specifies which gpu to use (or -1 for first available)
  """
    print(f"Running experiment with config {experiment_config} on GPU {gpu_ind}")

    # Init dataset with proper args.
    datasets_module = importlib.import_module("squat_recognizer.datasets")
    dataset_class_ = getattr(datasets_module, experiment_config["dataset"])
    dataset_args = experiment_config.get("dataset_args", {})
    dataset = dataset_class_(**dataset_args)
    dataset.load_or_generate_data()
    # TODO: print dataset.

    # TODO: Init network with proper args.
    network_module = importlib.import_module("fastai.vision.models")
    network_fn_ = getattr(network_module, experiment_config["network"])

    # Init model with proper args.
    models_module = importlib.import_module("squat_recognizer.models")
    model_class_ = getattr(models_module, experiment_config["model"])

    model = model_class_(dataset_class_, network_fn=network_fn_)

    # TODO: Print model.

    experiment_config["train_args"] = {
        **DEFAULT_TRAIN_ARGS,
        **experiment_config.get("train_args", {}),
    }

    stage_one = experiment_config["train_args"].get("stage_one", {})
    stage_two = experiment_config["train_args"].get("stage_two", {})

    learner = train_model(
        model=model, databunch=dataset.data, stage_one=stage_one, stage_two=stage_two, save_weights=save_weights,
    )

    if export:
        model.export(learner)


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, default=1, help="Provide index of GPU to use.")
    parser.add_argument(
        "--save",
        default=False,
        dest="save",
        action="store_true",
        help="If true, then final weights will be saved to canonical, version-controlled location",
    )

    parser.add_argument(
        "--export",
        type=bool,
        default=False,
        dest="export",
        help="If true, then the model will be exported to canonical, version-controlled location",
    )

    parser.add_argument(
        "experiment_config",
        type=str,
        help='Experiment JSON (\'{"dataset": "FvbsDataset", "model":  \
             "CnnClassificationModel", "network": "resnet50"} \'',
    )

    args = parser.parse_args()
    return args


def main():
    """Run experiment."""
    args = _parse_args()
    experiment_config = json.loads(args.experiment_config)
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{args.gpu}"
    run_experiment(experiment_config, args.save, args.export, args.gpu)


if __name__ == "__main__":
    main()
