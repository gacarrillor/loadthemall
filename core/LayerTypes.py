import enum


class LayerType(enum.Enum):
    VECTOR = enum.auto()
    RASTER = enum.auto()
    POINTCLOUD = enum.auto()
