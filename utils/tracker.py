
import torch
from ultralytics import YOLO


class Tracker:
    def __init__(self, model_path="models/yolov8n.pt", confidence=0.5, imgsz=640):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.imgsz = imgsz

        # Detect which device is available: 'cuda' (GPU) or 'cpu'.
        # This runs ONCE at startup, not per frame — device availability
        # doesn't change mid-session.
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Running inference on: {self.device.upper()}")

        # Explicitly move the model to the detected device.
        # Ultralytics does this internally too, but being explicit here
        # makes device usage visible and intentional in our own code,
        # rather than relying on implicit default behavior.
        self.model.to(self.device)

    def track(self, frame):
        results = self.model.track(
            frame,
            conf=self.confidence,
            imgsz=self.imgsz,
            persist=True,
            tracker="bytetrack.yaml",
            device=self.device,   # <-- explicitly pass device per call
            verbose=False
        )
        return results[0]