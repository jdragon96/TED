import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from ted.ui.coco_window import Coco_Window

form_class = uic.loadUiType("./ted/ui/mainwindow.ui")[0]

class MainWindow(QMainWindow, form_class):
  # UI Controls
  button_Coco2YoloSeg: QPushButton = None
  button_Coco2YoloObj: QPushButton = None
  
  __coco_window: Coco_Window = None

  ###Constructor #############################################################  
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.Init_Commands()

  ###Properties #############################################################
  @property
  def coco_window(self):
    if self.__coco_window is None:
      self.__coco_window = Coco_Window()
    return self.__coco_window
  @coco_window.setter
  def coco_window(self, value):
    raise NotImplementedError("입력을 허용하지 않는다.")
  
  ###Functions ###############################################################
  
  
  ###Command ###############################################################
  def Init_Commands(self):
    self.button_Coco2YoloSeg.clicked.connect(self.button_Coco2YoloSeg_Click)
    self.button_Coco2YoloObj.clicked.connect(self.button_Coco2YoloObj_Click)

  def button_Coco2YoloSeg_Click(self, event):
    self.coco_window.show()
    
  def button_Coco2YoloObj_Click(self, event):
    pass
  
  