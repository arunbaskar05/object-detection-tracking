
import cv2

from utils.tracker import Tracker
from utils.detector import Detector
from utils.visualization import draw_detections, draw_fps, draw_counts
from utils.fps_counter import FPSCounter
from utils.video_writer import VideoWriter
from utils.object_counter import ObjectCounter
from utils.ui_controller import UIController
from utils.input_selector import choose_video_source


WINDOW_NAME = "Real-Time Object Detection & Tracking"


def nothing(x):
    
    pass


def run_image_mode(source_path):

    print("Running detection on image...")

    detector = Detector(model_path="models/yolov8n.pt", confidence=0.5)

    frame = cv2.imread(source_path)
    if frame is None:
        print("Error: Could not load the image file.")
        return

    results = detector.detect(frame)
    frame = draw_detections(frame, results)

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.waitKey(1)  

    ui = UIController(window_name=WINDOW_NAME, screenshot_dir="outputs")

    cv2.imshow(WINDOW_NAME, frame)

    print("Press any key to close the window (screenshot auto-saved).")
    cv2.waitKey(0)

    ui.take_screenshot(frame)
    cv2.destroyAllWindows()

def run_video_mode(source, is_file_input):
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    MAX_DIMENSION = 720
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = min(MAX_DIMENSION / max(original_width, original_height), 1.0)
    frame_width = int(original_width * scale)
    frame_height = int(original_height * scale)

    print(f"Original resolution: {original_width}x{original_height}")
    print(f"Processing at: {frame_width}x{frame_height} (scale={scale:.2f})")

    tracker = Tracker(model_path="models/yolov8n.pt", confidence=0.5, imgsz=640)
    fps_counter = FPSCounter(window_size=30)
    video_writer = VideoWriter(
        output_dir="outputs",
        frame_width=frame_width,
        frame_height=frame_height,
        fps=20
    )
    object_counter = ObjectCounter()

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    
    ret, first_frame = cap.read()
    if not ret:
        print("Error: Could not read from video source.")
        cap.release()
        return

    if scale < 1.0:
        first_frame = cv2.resize(first_frame, (frame_width, frame_height))

    cv2.imshow(WINDOW_NAME, first_frame)
    cv2.waitKey(1)  

    ui = UIController(window_name=WINDOW_NAME, screenshot_dir="outputs")
    cv2.createTrackbar("Confidence x100", WINDOW_NAME, 50, 100, nothing)

    print("Controls: 'q'=quit | 'r'=toggle recording | 'f'=toggle fullscreen | 's'=screenshot")

    unique_total = 0
    unique_per_class = {}
    first_iteration = True

    while True:
        if first_iteration:
            
            frame = first_frame
            first_iteration = False
        else:
            ret, frame = cap.read()

            if not ret:
                if is_file_input:
                    print("Video file finished playing.")
                else:
                    print("Error: Failed to grab frame from webcam.")
                break

            if scale < 1.0:
                frame = cv2.resize(frame, (frame_width, frame_height))

        confidence = cv2.getTrackbarPos("Confidence x100", WINDOW_NAME) / 100.0
        confidence = max(confidence, 0.01)
        tracker.confidence = confidence

        fps = fps_counter.update()
        results = tracker.track(frame)
        per_frame_counts, unique_total, unique_per_class = object_counter.update(results)

        frame = draw_detections(frame, results)
        frame = draw_fps(frame, fps)
        frame = draw_counts(frame, per_frame_counts, unique_total)

        if ui.is_recording:
            video_writer.write(frame)

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            ui.take_screenshot(frame)

        if ui.handle_key(key):
            print("Quitting...")
            break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

    print(f"Video saved successfully at: {video_writer.output_path}")
    print(f"\n--- Session Summary ---")
    print(f"Total unique objects tracked: {unique_total}")
    for class_name, count in unique_per_class.items():
        print(f"  {class_name}: {count}")


def main():
    source, source_type = choose_video_source()

    if source_type == "image":
        run_image_mode(source)
    else:
        is_file_input = (source_type == "video")
        run_video_mode(source, is_file_input)


if __name__ == "__main__":
    main()