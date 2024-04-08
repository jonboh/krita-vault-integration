from PyQt5 import QtCore

active_document = Krita.instance().activeDocument()

width = active_document.width()
height = active_document.height()
expand_x = max(int(0.1 * width),1)
expand_y = max(int(0.1 * height),1)


active_document.setWidth(width+expand_x)

QtCore.qDebug("expand_canvas done")
