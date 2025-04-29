
import torch
import torch.nn as nn
from torchvision import models

# EfficientNetB0 pentru clasificarea panourilor solare
class EfficientNetB0(nn.Module):
    def __init__(self, num_classes=6):
        super().__init__()
        self.model = models.efficientnet_b0(weights=None)  # deja antrenat, deci nu e nevoie de weights
        self.model.classifier[1] = nn.Linear(self.model.classifier[1].in_features, num_classes)

    def forward(self, x):
        return self.model(x)
