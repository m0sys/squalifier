<h1 align="center">Welcome to squalifier 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
  <a href="documentation.md" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
</p>

> Front-squat vs Back-squat classification web app.

### 🏠 [Homepage](squalifier.com)

## Install

See [setup.md](https://github.com/mhd53/squalifier/blob/master/setup.md) to get started!

## Training Models

------------------------------------

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

👤 **morealfit**

* Github: [@mhd53](https://github.com/mhd53)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_