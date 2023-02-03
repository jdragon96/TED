from enum import Enum

class DataType(Enum):
  COCO=1
  YOLO=2
  VOC=3

class AI_TYPE(Enum):
  OBJECT_DETECTION = 1
  INSTANCE_SEGMENTATION = 2
  SEMANTIC_SEGMENTATION = 2