import torch
import torchvision.transforms as transforms
from PIL import Image
from ml_models.solar_panels_resnet9_model import ResNet9
from ml_models.efficientnetb0_model import EfficientNetB0
import logging
import sys

logger = logging.getLogger("uvicorn")

class_names = ['Bird-drop', 'Clean', 'Dusty', 'Electrical-damage', 'Physical-Damage', 'Snow-Covered']

# # Inițializare model
# if USE_MODEL == "resnet":
#     model = ResNet9(3, len(class_names))
#     model.load_state_dict(torch.load("ml_models/solar-panels-resnet9-model.pth", map_location=torch.device("cpu")))
# elif USE_MODEL == "efficientnet":
#     model = EfficientNetB0(num_classes=len(class_names))
#     state_dict = torch.load("ml_models/efficientnet_solar_model.pth", map_location=torch.device("cpu"))
#     # Adaugă prefixul 'model.' la fiecare cheie
#     new_state_dict = {"model." + k: v for k, v in state_dict.items()}
#     model.load_state_dict(new_state_dict)
# elif USE_MODEL == "vgg":
#     model = EfficientNetB0(num_classes=len(class_names))
#     state_dict = torch.load("ml_models/efficientnet_solar_model.pth", map_location=torch.device("cpu"))
#     # Adaugă prefixul 'model.' la fiecare cheie
#     new_state_dict = {"model." + k: v for k, v in state_dict.items()}
#     model.load_state_dict(new_state_dict)
# elif USE_MODEL == "mobilenet":
#     model = EfficientNetB0(num_classes=len(class_names))
#     state_dict = torch.load("ml_models/efficientnet_solar_model.pth", map_location=torch.device("cpu"))
#     # Adaugă prefixul 'model.' la fiecare cheie
#     new_state_dict = {"model." + k: v for k, v in state_dict.items()}
#     model.load_state_dict(new_state_dict)
# else:
#     raise ValueError("Model invalid")



# Transformări
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_image(image_path, model_name):
    if model_name == "resnet":
        logger.info("Using ResNet model")
        model = ResNet9(3, len(class_names))
        model.load_state_dict(torch.load("ml_models/solar-panels-resnet9-model.pth", map_location=torch.device("cpu")))
    elif model_name == "efficientnet":
        logger.info("Using eff model")
        model = EfficientNetB0(num_classes=len(class_names))
        state_dict = torch.load("ml_models/efficientnet_solar_model.pth", map_location=torch.device("cpu"))
        # Adaugă prefixul 'model.' la fiecare cheie
        new_state_dict = {"model." + k: v for k, v in state_dict.items()}
        model.load_state_dict(new_state_dict)
    elif model_name == "vgg":
        logger.info("Using vgg model")
        print("Using model vgg", file=sys.stdout, flush=True)
        model = EfficientNetB0(num_classes=len(class_names))
        state_dict = torch.load("ml_models/efficientnet_solar_model.pth", map_location=torch.device("cpu"))
        # Adaugă prefixul 'model.' la fiecare cheie
        new_state_dict = {"model." + k: v for k, v in state_dict.items()}
        model.load_state_dict(new_state_dict)
    elif model_name == "mobilenet":
        logger.info("Using mob model")
        model = EfficientNetB0(num_classes=len(class_names))
        state_dict = torch.load("ml_models/efficientnet_solar_model.pth", map_location=torch.device("cpu"))
        # Adaugă prefixul 'model.' la fiecare cheie
        new_state_dict = {"model." + k: v for k, v in state_dict.items()}
        model.load_state_dict(new_state_dict)
    else:
        raise ValueError("Model invalid")

    model.eval()

    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)
        return class_names[predicted.item()]
