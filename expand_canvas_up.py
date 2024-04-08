from PyQt5 import QtCore

active_document = Krita.instance().activeDocument()

height = active_document.height()
expand_y = max(int(0.1 * height),1)


active_document.setYOffset(active_document.yOffset()-expand_y)
active_document.setHeight(height+expand_y)

QtCore.qDebug("expand_canvas done")
