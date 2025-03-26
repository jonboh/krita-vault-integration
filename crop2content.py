from krita import QImage
from PyQt5 import QtCore


def point2pixel(coord, coord_res):
    """From https://api.kde.org/krita/html/classVectorLayer.html:
    Vector shapes all have their coordinates in points, which is a unit that represents 1/72th of an inch. Keep this in mind wen parsing the bounding box and position data."""
    return coord / 72 * coord_res


def crop2content(document):
    print("some")
    document = Krita.instance().activeDocument()
    xmins = list()
    xmaxs = list()
    ymins = list()
    ymaxs = list()
    xres = document.xRes()
    yres = document.yRes()
    for i, layer in enumerate(document.topLevelNodes()):
        if layer.type() == "paintlayer":
            xmin = layer.bounds().left()
            xmax = layer.bounds().right()
            ymin = layer.bounds().top()
            ymax = layer.bounds().bottom()
            xmins.append(xmin)
            xmaxs.append(xmax)
            ymins.append(ymin)
            ymaxs.append(ymax)
        elif layer.type() == "vectorlayer":
            for shape in layer.shapes():
                shape_box = shape.boundingBox()
                bottom = point2pixel(shape_box.bottom(), yres)
                top = point2pixel(shape_box.top(), yres)
                left = point2pixel(shape_box.left(), xres)
                right = point2pixel(shape_box.right(), xres)
                xmins.append(left)
                xmaxs.append(right)
                ymins.append(bottom)
                ymaxs.append(top)
    xmin = min(xmins)
    xmax = max(xmaxs)
    ymin = min(ymins)
    ymax = max(ymaxs)
    print(f"xmin: {xmin} xmax: {xmax} ymin: {ymin} ymax: {ymax}")
    # crop to dimensions
    document.setXOffset(int(xmin - 50))
    document.setYOffset(int(ymin - 50))
    document.setWidth(int(xmax - xmin + 100))
    document.setHeight(int(ymax - ymin + 100))


try:
    active_document = Krita.instance().activeDocument()
    crop2content(active_document)
    QtCore.qDebug(f"imported and run done")
    # crop2content()
except Exception as e:
    QtCore.qWarning(f"Failed to run crop2content with: {e}")

QtCore.qDebug(f"crop2content done")
