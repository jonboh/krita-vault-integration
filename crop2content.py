from PyQt5 import QtCore
from krita import QImage

def is_transparent(pixels, length):
    img_data = QImage(pixels, length, 1, QImage.Format_RGBA8888)
    for i in range(length):
        color = img_data.pixelColor(i, 0)
        if color.alpha()!=0:
            return False
    return True

def generate_edges(layer, xmin, xmax, ymin, ymax, xmin_pending, xmax_pending, ymin_pending, ymax_pending):
    vertical_left = layer.pixelData(xmin, ymin, 1, ymax-ymin) if xmin_pending else None
    horizontal_top = layer.pixelData(xmin, ymin, xmax-xmin, 1) if ymin_pending else None
    vertical_right = layer.pixelData(xmax, ymin, 1, ymax-ymin) if xmax_pending else None
    horizontal_bottom = layer.pixelData(xmin, ymax, xmax-xmin, 1) if ymax_pending else None
    return (vertical_left, ymax-ymin), (horizontal_top, xmax-xmin), (vertical_right, ymax-ymin), (horizontal_bottom, xmax-xmin)

def shallow_edges(document, layer):
    xmin = 0
    xmax = document.width()
    ymin = 0
    ymax = document.height()
    xmin_pending = True
    xmax_pending = True
    ymin_pending = True
    ymax_pending = True
    while xmin_pending or xmax_pending or ymin_pending or ymax_pending:
        vertical_left, horizontal_top, vertical_right, horizontal_bottom = generate_edges(
                layer, xmin, xmax, ymin, ymax, xmin_pending, xmax_pending, ymin_pending, ymax_pending)
        if xmin_pending:
            if is_transparent(*vertical_left):
                xmin+=1
            else:
                xmin_pending = False
        if xmax_pending:
            if is_transparent(*vertical_right):
                xmax-=1
                if xmax == xmin: # theres no conten
                    xmax = xmin+1
                    xmin_pending = False
                    xmax_pending = False
            else:
                xmax_pending = False
        if ymin_pending:
            if is_transparent(*horizontal_top):
                ymin+=1
            else:
                ymin_pending = False
        if ymax_pending:
            if is_transparent(*horizontal_bottom):
                ymax-=1
                if ymax == ymin: # theres no conten
                    ymax = ymin+1
                    ymin_pending = False
                    ymax_pending = False
            else:
                ymax_pending = False



    return xmin, xmax, ymin, ymax

def deep_edges(document, layer):
    # get current edges
    xmin, xmax, ymin, ymax = shallow_edges(document, layer)
    # walk children
    for i, child in enumerate(layer.childNodes()):
        xmin_c, xmax_c, ymin_c, ymax_c = deep_edges(document, child)
        xmin = min(xmin, xmin_c)
        xmax = max(xmax, xmax)
        ymin = min(ymin, ymin_c)
        ymax = min(ymax, ymax_c)
    QtCore.qDebug(f"xmin: {xmin} xmax: {xmax} ymin: {ymin} ymax: {ymax}")
    return xmin, xmax, ymin, ymax


def crop2content(document):
    document = Krita.instance().activeDocument()
    xmins = list()
    xmaxs = list()
    ymins = list()
    ymaxs = list()
    for i, layer in enumerate(document.topLevelNodes()):
        xmin, xmax, ymin, ymax = deep_edges(document, layer)
        xmins.append(xmin)
        xmaxs.append(xmax)
        ymins.append(ymin)
        ymaxs.append(ymax)
    xmin = min(xmins)
    xmax = max(xmaxs)
    ymin = min(ymins)
    ymax = max(ymaxs)
    QtCore.qDebug(f"xmin: {xmin} xmax: {xmax} ymin: {ymin} ymax: {ymax}")
    # crop to dimensions
    document.setXOffset(xmin)
    document.setYOffset(ymin)
    document.setWidth(xmax-xmin)
    document.setHeight(ymax-ymin)

