from PyQt5 import QtCore
try:
    from . import crop2content
except:
    QtCore.qWarning("failed to import crop2content")

QtCore.qDebug("imported krita_vault_integration")
