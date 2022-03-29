import os

import gui

#Required for QT x OpenCV
#for k, v in os.environ.items():
#    if k.startswith("QT_") and "cv2" in v:
#:        del os.environ[k]

if __name__ == "__main__":
    gui.begin()
