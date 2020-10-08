#!/bin/bash
MODEL_PATH="./squat_recognizer/exports/"
MODEL_NAME="2020-09-23_12-19-00_CnnClassificationModel_FvbsDataset_resnet34.pkl"
SAVE_MODEL_NAME="CnnClassificationModel_FvbsDataset_resnet34.pkl"

aws s3 cp "s3://squalifier/trained-models/""${MODEL_NAME}" "${MODEL_PATH}""${SAVE_MODEL_NAME}"