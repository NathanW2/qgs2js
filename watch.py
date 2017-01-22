from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
from subprocess import call


def file_changed(path):
    print('Reloading file..')
    call(["python", path])

fs_watcher = QFileSystemWatcher(['exp2js.py'])
fs_watcher.fileChanged.connect(file_changed)

app = QApplication([])
app.exec_()
