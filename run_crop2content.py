from PyQt5 import QtCore
import krita_vault_integration

try:
    active_document = Krita.instance().activeDocument()
    krita_vault_integration.crop2content.crop2content(active_document)
    QtCore.qDebug(f"imported and run done")
    # crop2content()
except Exception as e:
    QtCore.qWarning(f"Failed to run crop2content with: {e}")

QtCore.qDebug(f"crop2content done")
