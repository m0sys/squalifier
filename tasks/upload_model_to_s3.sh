#!/bin/bash
timestamp=$(date +%Y-%m-%d_%H-%M-%S)
model_name="_CnnClassificationModel_FvbsDataset_resnet34.pkl"
MODEL_PATH="./squat_recognizer/exports/CnnClassificationModel_FvbsDataset_resnet34.pkl"

aws s3 cp "${MODEL_PATH}" "s3://squalifier/trained-models/""${timestamp}""${model_name}"