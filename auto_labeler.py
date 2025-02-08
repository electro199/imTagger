import sys
from PySide6.QtCore import QThread, Signal, Slot
from PIL import Image
import torch
class Auto_Labbeler(QThread):
    result_signal = Signal(str)  # Signal to send data back to the main thread
    finished_signal = Signal()  # Signal to indicate that processing is finished

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = None
        self.feature_extractor = None
        self.image_path = ""

    def load_model(self) :
        
        from transformers import ViTFeatureExtractor, ViTForImageClassification
        
        self.model =  ViTForImageClassification.from_pretrained('google/vit-base-patch16-224', 
                                                #   num_labels=100,
                                                #   ignore_mismatched_sizes=True,
                                                #   map_location=torch.device('cpu') 
                                                  )

        self.feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')

         
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()
        
    def set_image_path(self, image_path):
        self.image_path = image_path

    def run(self):
        # Load and process the image
        if not self.model:
            self.load_model()

        if self.image_path:
            image = Image.open(self.image_path).convert('RGB').resize((244,244))
            processed_image = self.feature_extractor(images=image, return_tensors="pt")
            processed_image = {k: v.to(self.device) for k, v in processed_image.items()}
            with torch.no_grad():
                outputs = self.model(**processed_image)

            predicted_class_idx = torch.argmax(outputs.logits, dim=-1).item()
            predicted_class =  self.model.config.id2label[predicted_class_idx]
            
            self.result_signal.emit(predicted_class)
        self.finished_signal.emit()