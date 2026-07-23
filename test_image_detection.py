
import cv2
from utils.detector import Detector

def main():
    # Initialize our detector wrapper.
    # First run will auto-download yolov8n.pt (~6MB, the "nano" model —
    # smallest and fastest, ideal for real-time use on CPU).
    detector = Detector(model_path="models/yolov8n.pt", confidence=0.5)

    # Load a test image from disk. Replace with any .jpg/.png you have,
    # or we can grab one from the internet for testing.
    image = cv2.imread("assets/test.jpg")

    if image is None:
        print("Error: Could not load image. Check the path.")
        return

    # Run detection
    results = detector.detect(image)

    # results.plot() returns a NEW image with boxes/labels/scores
    # already drawn on it by Ultralytics' built-in visualizer.
    # (We'll write our OWN custom drawing code in visualization.py later,
    # but this confirms detection itself is working first.)
    annotated_image = results.plot()

    # Display it
    cv2.imshow("YOLO Detection Test", annotated_image)
    cv2.waitKey(0)  # Wait indefinitely until any key is pressed
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()