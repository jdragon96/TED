from ted.core.coco import CocoModule
from ted.core.yolo import YoloModule
from ted.core.enum import AI_TYPE
from ted.ui import mainwindow
from PyQt5.QtWidgets import *
import sys
# a = CocoModule.load(r"C:\Users\wodyd\Desktop\MyGit\AI\TED\example\instances_default.json")
# b = CocoModule.transform_to_yolo(a, AI_TYPE.INSTANCE_SEGMENTATION)
# c = YoloModule.save(b)
# print(c)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = mainwindow.MainWindow()
    myWindow.show()
    app.exec_()