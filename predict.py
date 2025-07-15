import torch
import torchvision.transforms as transforms
from PIL import Image
from ml_models.resnet_model import ResNet
from ml_models.efficientnetb0_model import EfficientNetB0
from ml_models.vgg16_model import VGG16
import logging
import sys
from ultralytics import YOLO
import os
import cv2
import tensorflow as tf
import numpy as np

logger = logging.getLogger("uvicorn")

class_names = ['Bird-drop', 'Clean', 'Dusty', 'Electrical-damage', 'Physical-Damage', 'Snow-Covered']

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    # transforms.Resize((112, 112)),
    transforms.ToTensor()
])

def predict_image(image_path, model_name):

    file_ext = os.path.splitext(image_path)[-1].lower()
    yolo_model = YOLO("ml_models/yolo_panel_detection.pt")

    if file_ext in ['.mp4', '.avi', '.mov', '.mkv']:
        logger.info(f"Detectat fișier video: {image_path}")
        cap = cv2.VideoCapture(image_path)
        frame_index = 0
        detected = False
        selected_frame_path = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_index % 5 == 0:
                temp_frame_path = f"temp_frame_{frame_index}.jpg"
                cv2.imwrite(temp_frame_path, frame)
                result = yolo_model(temp_frame_path)[0]

                if len(result.boxes) > 0:
                    logger.info(f"Panou detectat în cadrul {frame_index}")
                    detected = True
                    selected_frame_path = temp_frame_path
                    break
                else:
                    os.remove(temp_frame_path)

            frame_index += 1

        cap.release()

        if not detected:
            logger.info("Niciun panou detectat în video")
            return "Not-Detected"

        image_path = selected_frame_path

    else:
        yolo_result = yolo_model(image_path)[0]
        if len(yolo_result.boxes) == 0:
            return "Not-Detected"

    if model_name == "resnet":
        logger.info("Using ResNet model")
        model = ResNet(num_classes=len(class_names))
        state_dict = torch.load("ml_models/resnet_model.pth", map_location=torch.device("cpu"))
        new_state_dict = {"model." + k: v for k, v in state_dict.items()}
        model.load_state_dict(new_state_dict)
        # model.load_state_dict(torch.load("custom_resnet_model.pth", map_location=torch.device("cpu")))
        # model.load_state_dict(torch.load("ml_models/solar-panels-resnet9-model.pth", map_location=torch.device("cpu")))
        # model.load_state_dict(torch.load("ml_models/resnet_model_v2.pth", map_location=torch.device("cpu")))
        # model.load_state_dict(torch.load("ml_models/resnet_model_final_licenta.pth", map_location=torch.device("cpu")))
    elif model_name == "efficientnet":
        logger.info("Using eff model")
        model = EfficientNetB0(num_classes=len(class_names))
        state_dict = torch.load("ml_models/efficientnet_solar_model.pth", map_location=torch.device("cpu"))
        new_state_dict = {"model." + k: v for k, v in state_dict.items()}
        model.load_state_dict(new_state_dict)
    elif model_name == "vgg":
        logger.info("Using VGG model")
        model = VGG16(num_classes=len(class_names))
        state_dict = torch.load("ml_models/vgg_model.pth", map_location=torch.device("cpu"))
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
