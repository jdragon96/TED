import sys
sys.path.append(r"C:\Users\USER\Desktop\Projects\Yolov5\Cameleon")
from core.base import Base
from core.format import coco_format
from core.format import yolo_format
from core.yolo import YoloModule

from core import enum as E

from types import GenericAlias
import json

class CocoModule(Base):

  # https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/md-coco-overview.html
  @staticmethod
  def load(filename: str) -> coco_format.CocoFormat:
    try:
      # read-only
      loaded_coco = json.load(open(filename, mode="r"))
      CocoTypes = coco_format.CocoFormat.__annotations__
      parsed_data = coco_format.CocoFormat()

      # try parse 
      for key in CocoTypes.keys():

        # info
        if key == "info":
          new_info = coco_format.Coco_Info()
          for info_key in coco_format.Coco_Info.__annotations__:
            new_info.__setattr__(info_key, loaded_coco[key][info_key])
          parsed_data.__setattr__(key, new_info)

        # licenses
        elif key == "licenses":
          container = []

          for row in loaded_coco[key]:
            new_license = coco_format.Coco_Licenses()

            for license_key in coco_format.Coco_Licenses.__annotations__:
              new_license.__setattr__(license_key, row[license_key])
            container.append(new_license)
          parsed_data.__setattr__(key, container)

        elif key == "images":
          container = []

          for row in loaded_coco[key]:
            new_images = coco_format.Coco_Images()

            for images_key in coco_format.Coco_Images.__annotations__:
              new_images.__setattr__(images_key, row[images_key])
            container.append(new_images)
          parsed_data.__setattr__(key, container)

        elif key == "annotations":
          container = []

          for row in loaded_coco[key]:
            new_annotations = coco_format.Coco_Annotations()

            for annotations_key in coco_format.Coco_Annotations.__annotations__:
              new_annotations.__setattr__(annotations_key, row[annotations_key])
            container.append(new_annotations)
          parsed_data.__setattr__(key, container)

        elif key == "categories":
          container = []

          for row in loaded_coco[key]:
            new_categories = coco_format.Coco_Categories()

            for caterories_key in coco_format.Coco_Categories.__annotations__:
              new_categories.__setattr__(caterories_key, row[caterories_key])
            container.append(new_categories)
          parsed_data.__setattr__(key, container)

        else:
          raise NotImplementedError("Not valid Coco Fotmat data!!")

      return parsed_data

    except Exception as e:
      print("Failed COCO label")
      return None
  
  @staticmethod
  def transform_to_yolo(data: coco_format.CocoFormat, ai_type: E.AI_TYPE) -> yolo_format.YoloFormat:
    hashmap = CocoModule.gen_hashmap_for_image(data)
    yolo_hash: dict(int, yolo_format.YoloFormat) = {}

    if ai_type == E.AI_TYPE.OBJECT_DETECTION:
      pass

    elif ai_type == E.AI_TYPE.INSTANCE_SEGMENTATION:
      for annotation in data.annotations:
        if yolo_hash.get(annotation.image_id) is None: 
          yolo_hash[annotation.image_id] = yolo_format.YoloFormat(
            image_name = hashmap[annotation.image_id].image_name,
            labels=[])

        seg = []
        for index in range(len(annotation.segmentation[0])):
          seg.append(
            YoloModule.YoloCoordX(annotation.segmentation[0][index], hashmap[annotation.image_id].width) if index % 2 == 0 
            else YoloModule.YoloCoordX(annotation.segmentation[0][index], hashmap[annotation.image_id].height))

        yolo_hash[annotation.image_id].labels.append(
          yolo_format.Yolo_Label(
            category_id=annotation.category_id,
            segmetation=seg
          )
        )

    elif ai_type == E.AI_TYPE.SEMANTIC_SEGMENTATION:
      pass
  
    return yolo_hash

  @staticmethod
  def gen_hashmap_for_image(data: coco_format.CocoFormat):
    """ 
    generate image id hash table using parsed COCO data.

    - key: iamge id
    - value: iamge width, height
    {
      1 : {width: 100, height: 400},
      2 : {width: 100, height: 400},
      ...
    }
    """
    hash_map = {}
    for image in data.images:
      c = coco_format.Coco_HashmapValue(
        height=image.height,
        width=image.width,
        image_name = image.file_name
      )
      hash_map[image.id] = c
    return hash_map

if __name__ == "__main__":
  a = CocoModule.load(r"C:\Users\USER\Desktop\Projects\Yolov5\Data\GagueInstance\instances_default.json")
  b = CocoModule.transform_to_yolo(a, E.AI_TYPE.INSTANCE_SEGMENTATION)
  print(b)