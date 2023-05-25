# capture nuke viewer for screenshot tool

nuke.activeViewer().node().capture("C:/temp/file5.jpg")

from PySide2 import QtCore
from PySide2.QtCore import *

fpth = "/Users/dansturm/Desktop/capture.jpg"

timg = Image.open("/Users/dansturm/Desktop/capture.jpg")

PySide6.QtGui.QImage.load(/Users/dansturm/Desktop/capture.jpg[, format=None])

simg = timg.scaledToHeight(1800, mode=Qt.SmoothTransformation)
cimg = simg.copy(ssx, 0, swid, shig)  
cimg.save(fpth, "PNG")