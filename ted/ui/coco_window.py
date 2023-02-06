import sys
import os
from shutil import copyfile

from ted.core.coco import CocoModule
from ted.core.yolo import YoloModule
from ted.core.enum import AI_TYPE

from ted.model.packet_base import MethodPacket
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("./ted/ui/coco_windowui.ui")[0]

class Coco_Window(QMainWindow, form_class):
  # UI Controls
  button_CocoPath: QPushButton = None
  button_ImagePath: QPushButton = None
  button_SavePath: QPushButton = None
  button_SaveYoloSeg: QPushButton = None
  label_CocoPath: QLabel = None
  label_ImagePath: QLabel = None
  label_SavePath: QLabel = None
  edit_TrainDataRatio: QLineEdit = None
  
  ###Constructor #############################################################  
  def __init__(self):
      super().__init__()
      self.setupUi(self)
      self.Init_Commands()
        
        
  ###Properties #############################################################

        
  ###Functions ###############################################################
  def FileDialogOpen(self, accepted_format=["json"]) -> str:
    fname = QFileDialog.getOpenFileName(self, "Open File", "./")
    return fname[0]
  def FolderDialogOpen(self) -> str:
    fname = QFileDialog.getExistingDirectory(self, "Select Directory")
    return fname
  def MakeYoloSaveFolder(self, path) -> bool:
    try:
      os.mkdir(rf"{path}\train")
      os.mkdir(rf"{path}\train\images")
      os.mkdir(rf"{path}\train\labels")
      os.mkdir(rf"{path}\val")
      os.mkdir(rf"{path}\val\images")
      os.mkdir(rf"{path}\val\labels")
      return True
    except Exception as e:
      return False
  def ValidationCheck_YoloSaveFolder(self, path) -> bool:
      if not os.path.exists(rf"{path}"): return False
      if not os.path.exists(rf"{path}\train"): return False
      if not os.path.exists(rf"{path}\train\images"): return False
      if not os.path.exists(rf"{path}\train\labels"): return False
      if not os.path.exists(rf"{path}\val"): return False
      if not os.path.exists(rf"{path}\val\images"): return False
      if not os.path.exists(rf"{path}\val\labels"): return False
      return True
  
  ###Command ###############################################################
  def Init_Commands(self):
    self.button_CocoPath.clicked.connect(self.button_CocoPath_Click)
    self.button_ImagePath.clicked.connect(self.button_ImagePath_Click)
    self.button_SavePath.clicked.connect(self.button_SavePath_Click)
    self.button_SaveYoloSeg.clicked.connect(self.button_SaveYoloSeg_Click)
  
  def button_CocoPath_Click(self, event):
    fname = self.FileDialogOpen()
    self.label_CocoPath.setText(fname)
    
  def button_ImagePath_Click(self, event):
    fname = self.FolderDialogOpen()
    self.label_ImagePath.setText(fname)
    
  def button_SavePath_Click(self, event):
    fname = self.FolderDialogOpen()
    self.label_SavePath.setText(fname)
    
  def button_SaveYoloSeg_Click(self, event):
    """
    "SavePath"
      ├───train
      │     ├──images ... 
      │     └──labels ...
      └───val
            ├──images ...
            └──labels ...
    """
    # 1. create folders for Yolov5
    save_path = self.label_SavePath.text()
    image_path = self.label_ImagePath.text()
    if self.edit_TrainDataRatio.text() is None: return
    train_ratio = str(self.edit_TrainDataRatio.text())
    
    # if not train_ratio.isdigit(): return
    train_ratio = float(train_ratio)
    if save_path is None: return
    if not os.path.exists(save_path):
      return
    if not self.ValidationCheck_YoloSaveFolder(save_path):
      self.MakeYoloSaveFolder(save_path)
      
    a = CocoModule.load(fr"{self.label_CocoPath.text()}")
    yolo_data = CocoModule.transform_to_yolo(a, AI_TYPE.INSTANCE_SEGMENTATION)
    image_ids = list(yolo_data.keys())
    
    # 2. copy images to train/images and val/images
    # 2-1 split data based on the number of train data ratio
    image_files = os.listdir(fr"{image_path}")
    num_of_train_images = int(len(yolo_data) * train_ratio)
    train_image_path = os.path.join(save_path, "train", "images")
    train_label_path = os.path.join(save_path, "train", "labels")
    val_image_path = os.path.join(save_path, "val", "images")
    val_label_path = os.path.join(save_path, "val", "labels")
    
    # save train label
    for image_id in image_ids[:num_of_train_images]:
      # 1. copy to train image folder.
      copyfile(
        f"{os.path.join(image_path, yolo_data[image_id].image_name)}", 
        f"{os.path.join(train_image_path, yolo_data[image_id].image_name)}")
      
      # 2. save label data that copied image in step 1 before.
      YoloModule.save_one(yolo_data[image_id], train_label_path)
    
    # save valid label
    for image_id in image_ids[num_of_train_images:]:
      # 1. copy to val image folder.
      copyfile(
        f"{os.path.join(image_path, yolo_data[image_id].image_name)}", 
        f"{os.path.join(val_image_path, yolo_data[image_id].image_name)}")
      
      # 2. save label data that copied image in step 1 before.
      YoloModule.save_one(yolo_data[image_id], val_label_path)

    # and create .yaml file
    YoloModule.create_yaml("my_yolo", save_path, os.path.join(save_path, "train"), os.path.join(save_path, "label"))