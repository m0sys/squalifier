"""Functions to export specific model weights from the canoncial weight directory"""

import argparse
from argparse import Namespace

from training.training_utils import export_model_from_weights


def export_cnn_classification_model(stage: str) -> None:
    weight_str = "CnnClassificationModel_FvbsDataset_resnet34_weights_" + stage + ".pth"
    export_model_from_weights(weight_str)


def _parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", type=str, default="stage-2", help="Provide the weight's stage.")
    args = parser.parse_args()
    return args


def main() -> None:
    """Export weights."""
    args = _parse_args()
    export_cnn_classification_model(args.stage)


if __name__ == "__main__":
    main()
