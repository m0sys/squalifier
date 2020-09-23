"""Utility functions for test suite."""


def load_all_images():
    pass


def get_label(idx) -> str:
    if idx % 2 == 0:
        return "back-squat"
    else:
        return "front-squat"
