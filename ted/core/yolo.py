import os
import sys
import yaml
from ted.model import yolo_format

class YoloModule:

  @staticmethod
  def yolo_coord_x(coord_x, image_width) -> float:
    return round(coord_x / image_width, 3)
  
  @staticmethod
  def yolo_coord_y(coord_y, image_height) -> float:
    return round(coord_y / image_height, 3)
  
  @staticmethod
  def save(data: yolo_format.YoloSave, path: str = ".") -> bool:
    try:
      # save yolo label data
      filename = ""
      new_line = ""
      for image_id in data:
        filename = os.path.splitext(data[image_id].image_name)[0]
        f = open(os.path.join(path, f"{filename}.txt"), 'w')
        
        # sort label based on category_id
        data[image_id].labels.sort(key=lambda x: x.category_id, reverse=False)
        
        # write labels
        for label in data[image_id].labels:
          new_line = "{} {}{}".format(label.category_id, f" ".join([f"{coord}" for coord in label.segmetation])[:-1], "\n")
          f.write(new_line)
        f.close()
        
    except Exception as e:
        print(e)
        
  @staticmethod
  def save_split(data: yolo_format.YoloSave, train_path, val_path, train_length) -> bool:
    try:
      # # save yolo label data
      # filename = ""
      # new_line = ""
      # for image_id in data:
      #   filename = os.path.splitext(data[image_id].image_name)[0]
      #   f = open(os.path.join(save, f"{filename}.txt"), 'w')
        
      #   # sort label based on category_id
      #   data[image_id].labels.sort(key=lambda x: x.category_id, reverse=False)
        
      #   # write labels
      #   for label in data[image_id].labels:
      #     new_line = "{} {}{}".format(label.category_id, f" ".join([f"{coord}" for coord in label.segmetation])[:-1], "\n")
      #     f.write(new_line)
      #   f.close()
      pass
        
    except Exception as e:
        print(e)
        
  @staticmethod
  def save_one(row: yolo_format.YoloFormat, save_path):
    try:
      # save yolo label data
      new_line = ""
      filename = os.path.splitext(row.image_name)[0]
      
      f = open(os.path.join(save_path, f"{filename}.txt"), 'w')
      
      # sort label based on category_id
      row.labels.sort(key=lambda x: x.category_id, reverse=False)
      
      # write labels
      for label in row.labels:
        new_line = "{} {}{}".format(label.category_id, f" ".join([f"{coord}" for coord in label.segmetation])[:-1], "\n")
        f.write(new_line)
      f.close()
      
    except Exception as e:
        print(e)

  @staticmethod
  def create_yaml(file_name, save_path, train_path, val_path):
    try:
      obj = {}
      obj["train"] = train_path
      obj["val"] = val_path
      obj["names"] = None

      with open(os.path.join(save_path, f"{file_name}.yaml"), "w") as f:
        yaml.dump(obj, f)
      return True
      
    except Exception as e:
      return False
