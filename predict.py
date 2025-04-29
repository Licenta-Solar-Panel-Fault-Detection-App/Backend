import torch
import torchvision.transforms as transforms
from PIL import Image
from ml_models.solar_panels_resnet9_model import ResNet9
from ml_models.efficientnetb0_model import EfficientNetB0

# Alege modelul activ:
USE_MODEL = "efficientnet"  # sau "resnet"

# Setare clase
class_names = ['Bird-drop', 'Clean', 'Dusty', 'Electrical-damage', 'Physical-Damage', 'Snow-Covered']

# Inițializare model
if USE_MODEL == "resnet":
    model = ResNet9(3, len(class_names))
    model.load_state_dict(torch.load("ml_models/solar-panels-resnet9-model.pth", map_location=torch.device("cpu")))
elif USE_MODEL == "efficientnet":
    model = EfficientNetB0(num_classes=len(class_names))
    state_dict = torch.load("ml_models/efficientnet_solar_model.pth", map_location=torch.device("cpu"))
    # Adaugă prefixul 'model.' la fiecare cheie
    new_state_dict = {"model." + k: v for k, v in state_dict.items()}
    model.load_state_dict(new_state_dict)
else:
    raise ValueError("Model invalid")

model.eval()

# Transformări
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)
        return class_names[predicted.item()]
