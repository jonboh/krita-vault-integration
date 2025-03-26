To iterate over the scripts use krita `Scripter`, load the file that you are iterating over and use `Alt+r` and `Ctrl+r` to refresh and rerun the script.

For example to iterate over `crop2content` modify the file to run the function in it:
```python
# the rest of the file

# this will run when the script is called in Scripter. You can use prints to see the output in Scripter
# debug messages in QtCore.qDebug are only shown in the shell that runs krita.

try:
    active_document = Krita.instance().activeDocument()
    crop2content(active_document)
    QtCore.qDebug(f"imported and run done")
    # crop2content()
except Exception as e:
    QtCore.qWarning(f"Failed to run crop2content with: {e}")

QtCore.qDebug(f"crop2content done")


```
