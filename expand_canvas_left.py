from PyQt5 import QtCore

active_document = Krita.instance().activeDocument()

width = active_document.width()
expand_x = max(int(0.1 * width),1)


active_document.setXOffset(active_document.xOffset()-expand_x)
active_document.setWidth(width+expand_x)

QtCore.qDebug("expand_canvas done")
