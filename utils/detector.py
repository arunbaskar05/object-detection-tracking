from ultralytics import YOLO  # Ultralytics' high-level YOLO API


class Detector:
    """
    A thin wrapper around the Ultralytics YOLO model.
    Loading the model is expensive (reads weights from disk into memory/GPU),
    so we do it ONCE in __init__, not on every frame.
    """

    def __init__(self, model_path="models/yolov8n.pt", confidence=0.5):
        """
        model_path: path to the pretrained YOLO weights file (.pt)
        confidence: minimum confidence score to keep a detection
        """
        # Load the YOLO model. On first run, if the file doesn't exist locally,
        # Ultralytics automatically downloads it from their servers.
        self.model = YOLO(model_path)

        # Store the confidence threshold for filtering weak detections
        self.confidence = confidence

    def detect(self, frame):
        """
        Runs YOLO inference on a single frame (image).

        frame: a NumPy array (the image), e.g., shape (480, 640, 3)
        returns: the raw Ultralytics 'Results' object for this frame,
                 which contains boxes, class ids, and confidence scores.
        """
        # verbose=False stops Ultralytics from printing detection logs
        # for every single frame (would flood our terminal in a video loop)
        results = self.model(frame, conf=self.confidence, verbose=False)

        # model() returns a list (one Results object per image passed in).
        # Since we only passed ONE frame, we grab the first (and only) result.
        return results[0]