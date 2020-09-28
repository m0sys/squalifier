#!/bin/bash
docker run --network=host -p 5000:5000 --name api -it --rm squat_recognizer_api