
import cv2

from utils.tracker import Tracker
from utils.visualization import draw_detections, draw_fps, draw_counts
from utils.fps_counter import FPSCounter
from utils.video_writer import VideoWriter
from utils.object_counter import ObjectCounter
from utils.ui_controller import UIController


WINDOW_NAME = "Real-Time Object Detection & Tracking"


def nothing(x):
   
    pass


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    tracker = Tracker(model_path="models/yolov8n.pt", confidence=0.5, imgsz=640)
    fps_counter = FPSCounter(window_size=30)
    video_writer = VideoWriter(
        output_dir="outputs",
        frame_width=frame_width,
        frame_height=frame_height,
        fps=20
    )
    object_counter = ObjectCounter()

    # Create the named window FIRST, before adding a trackbar to it —
    # cv2.createTrackbar requires the window to already exist.
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    ui = UIController(window_name=WINDOW_NAME, screenshot_dir="outputs")

    # Create the confidence slider.
    # Arguments: trackbar name, window name, initial value, max value, callback
    # OpenCV trackbars only support INTEGER values, so we use 0-100
    # to represent confidence 0.00-1.00, then divide by 100 when reading it.
    cv2.createTrackbar("Confidence x100", WINDOW_NAME, 50, 100, nothing)

    print("Webcam opened successfully.")
    print("Controls: 'q'=quit | 'r'=toggle recording | 'f'=toggle fullscreen | 's'=screenshot")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Read the current slider value and convert it back to a 0.0-1.0 float
        confidence = cv2.getTrackbarPos("Confidence x100", WINDOW_NAME) / 100.0
        # Guard against a confidence of exactly 0, which would let through
        # every single detection regardless of quality (not meaningful)
        confidence = max(confidence, 0.01)
        tracker.confidence = confidence  # Update it live, no restart needed

        fps = fps_counter.update()
        results = tracker.track(frame)
        per_frame_counts, unique_total, unique_per_class = object_counter.update(results)

        frame = draw_detections(frame, results)
        frame = draw_fps(frame, fps)
        frame = draw_counts(frame, per_frame_counts, unique_total)

        # Only write to the output video file if recording is currently ON
        if ui.is_recording:
            video_writer.write(frame)

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF

        # Screenshot needs the actual frame, so we handle it here directly
        if key == ord('s'):
            ui.take_screenshot(frame)

        # Let the UI controller handle quit/recording-toggle/fullscreen-toggle
        should_quit = ui.handle_key(key)
        if should_quit:
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


if __name__ == "__main__":
    main()