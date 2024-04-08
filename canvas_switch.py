from PyQt5 import QtCore

workspaces = Application.resources("workspace")

Application.activeWindow().views()[0].activateResource(workspaces["Default"])

QtCore.qDebug(f"{workspaces}")
