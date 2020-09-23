#!/bin/bash
python training/run_experiment.py --save '{"dataset": "FvbsDataset",
                                           "model": "CnnClassificationModel",
                                           "network": "resnet34",
                                           "train_args": {
                                             "stage_one": {
                                               "one_cycle": 1,
                                               "epochs": 10},
                                             "stage_two": {
                                               "unfreeze": 1,
                                               "one_cycle": 1,
                                               "max_lr_start": 3e-4,
                                               "max_lr_end": 3e-3,
                                               "epochs": 15
                                             }
                                           }
                                          }'

# Last experiment: 2020-09-01 -> error-rate = 0.0675