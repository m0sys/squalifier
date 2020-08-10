"""Dataset class to be extended by dataset-specific classes."""
from pathlib import Path as path
import argparse
import os
import zipfile

from squat_recognizer import utils