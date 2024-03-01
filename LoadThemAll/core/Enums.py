from enum import Enum


class EnumLoadThemAllResult(Enum):
    SUCCESS = 1  # Load Layers was run, although it could've loaded layers or not
    CANCELLED = 9  # The task was cancelled by the user
