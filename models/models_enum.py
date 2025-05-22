from enum import Enum

class ModelEnum(str, Enum):
    resnet = "resnet"
    vgg = "vgg"
    efficientnet = "efficientnet"
    mobilenet = "mobilenet"
