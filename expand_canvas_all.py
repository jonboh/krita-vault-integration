from PyQt5 import QtCore

active_document = Krita.instance().activeDocument()

width = active_document.width()
height = active_document.height()
expand_x = max(int(0.1 * width),1)
expand_y = max(int(0.1 * height),1)


active_document.setXOffset(active_document.xOffset()-expand_x)
active_document.setYOffset(active_document.yOffset()-expand_y)
active_document.setWidth(width+2*expand_x)
active_document.setHeight(height+2*expand_y)

QtCore.qDebug("expand_canvas done")
