from dataclasses import dataclass
from typing import List

@dataclass
class Coco_ImageHash:
    width: int = None
    height: int = None
    image_name: str = None

# https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/md-coco-overview.html
@dataclass
class Coco_Licenses:
    name: str = None
    id: int = None
    url: str = None

@dataclass
class Coco_Info:
    contributor: str = None
    date_created: str = None
    description: str = None
    url: str = None
    version: str = None
    year: str = None

@dataclass
class Coco_Categories:
    id: int = None
    name: str = None
    supercategory: str = None

@dataclass
class Coco_Images:
    id: int = None
    width: int = None
    height: int = None
    file_name: str = None
    license: int = None
    flickr_url: str = None
    coco_url: str = None
    date_captured: int = None

@dataclass
class Coco_Annotations:
    id: int = None
    image_id: int = None
    category_id: int = None
    segmentation: List[List[float]] = None
    area: float = None
    bbox: List[float] = None


@dataclass
class CocoFormat:
    info: Coco_Info  = None
    licenses: List[Coco_Licenses] = None
    images: List[Coco_Images] = None
    annotations: List[Coco_Annotations] = None
    categories: List[Coco_Categories] = None