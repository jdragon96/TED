class YoloModule:

    @staticmethod
    def YoloCoordX(coord_x, image_width) -> float:
        return coord_x / image_width
    @staticmethod
    def YoloCoordY(coord_y, image_height) -> float:
        return coord_y / image_height