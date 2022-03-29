import os
import cv2

#Required for QT x OpenCV
for k, v in os.environ.items():
    if k.startswith("QT_") and "cv2" in v:
        del os.environ[k]

from . import *
