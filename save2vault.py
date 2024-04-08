import os
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

import krita_vault_integration

QtCore.qDebug(f"Executing save2vault")


def save(filename):
    QtCore.qInfo(f"saving {filename} project")
    active_document.setBatchmode(True)  # no popups while saving
    active_document.saveAs(filename[:-4] + ".png")
    active_document.saveAs(filename)


class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super(SaveDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Save File")
        self.setGeometry(100, 100, 300, 100)
        layout = QVBoxLayout()
        self.filename_edit = QLineEdit(self)
        self.filename_edit.setPlaceholderText("Enter a valid filename")
        layout.addWidget(self.filename_edit)
        self.warning_label = QLabel(self)
        layout.addWidget(self.warning_label)
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

    def save_file(self):
        filename = self.filename_edit.text()
        if not filename:
            self.warning_label.setText("Please enter a filename.")
            return
        full_filename = os.getenv("VAULT_LOCATION") + "/files/" + filename + ".kra"
        if os.path.exists(full_filename):
            QMessageBox.warning(
                self, "Warning", "File already exists. Please choose a different name."
            )
            return
        save(full_filename)
        self.accept()  # Close the dialog with an accept status.


try:
    active_document = Krita.instance().activeDocument()

    if active_document:
        krita_vault_integration.crop2content.crop2content(active_document)
        filename = active_document.fileName()
        if filename:
            save(filename)
        else:
            dialog = SaveDialog()
            if dialog.exec_() == QDialog.Accepted:
                QtCore.qDebug(f"save2vault saved new file to vault")
            else:
                QtCore.qDebug(f"save2vault cancelled")

    else:
        QtCore.qWarning(f"No active document")
except Exception as e:
    QtCore.qWarning(f"Failed to run save2vault with: {e}")

QtCore.qDebug(f"save2vault done")
