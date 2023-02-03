from dataclasses import dataclass

@dataclass
class Yolo_BBox:
    xmin: float = None
    xmax: float = None
    ymin: float = None
    ymax: float = None

@dataclass
class Yolo_Points:
    x: float = None
    y: float = None

@dataclass
class Yolo_Label:
    label: int = None
    category_id: int = None
    segmetation: list[float] = None
    bbox: Yolo_BBox = None

@dataclass
class YoloFormat:
    image_name: str = None
    labels: list[Yolo_Label] = None