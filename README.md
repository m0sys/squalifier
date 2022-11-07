<h1 align="center">Welcome to squalifier 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
  <a href="documentation.md" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
</p>

> Front-squat vs Back-squat classification web app.

See [notebooks](https://github.com/m0sys/squalifier/tree/master/notebooks) for model demo.

This Deeplearning application was trained on a small curated dataset of images crawled off of
google using a pretrained Resnet34 as the base. Click [here](https://github.com/m0sys/resnet-from-torch/blob/master/model/model.py) or [here](https://github.com/m0sys/retinanet-from-torch/blob/master/model/backbone/resnet.py) to see an
example implementation of Resnet models.

## Install

See [setup.md](https://github.com/m0sys/squalifier/blob/master/setup.md) to get started!

## Training Models

---

To train models run the following:

### CNN Classification Model

```shell
python training/run_experiment.py --save '{"dataset": "FvbsDataset", "model": "CnnClassificationModel", "network": "resnet34"}'
```

or

```shell
python ./tasks/train_simple_cnn_classification_model_on_fvbs.sh
```

### World Class CNN Classification Model (8-10% error rate)

```shell
python ./tasks/train_world_class_cnn_classification_model_on_fvbs.sh
```

## Usage

```sh
see setup.md
```

## Run tests

```sh
test/tests.py
```

## Author

👤 **m0sys**

- Github: [@m0sys](https://github.com/m0sys)

## Show your support

Give a ⭐️ if this project helped you!

---
