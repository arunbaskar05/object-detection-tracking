# Real-Time Object Detection and Tracking System

A real-time computer vision system that detects and tracks multiple objects
across live webcam feeds, uploaded video files, and static images, using
YOLOv8 for detection and ByteTrack for multi-object tracking. Built as
part of the CodeAlpha internship program.

## Features

- 🎥 Three input modes: live webcam, uploaded video file, or uploaded image
- 🎯 Real-time object detection using YOLOv8 (COCO 80-class pretrained)
- 🆔 Persistent multi-object tracking with unique IDs (ByteTrack)
- 🎨 Unique color per tracked object (or per class, in image mode) for
  easy visual distinction
- 📊 Live FPS counter (smoothed rolling average)
- 🔢 Per-frame and unique (session-total) object counting, per class
- 💾 Automatic annotated video output saving
- 📸 On-demand screenshot capture (video mode) / auto-saved result (image mode)
- ⏺️ Toggleable recording (start/stop without restarting the app)
- 🖥️ Full-screen display mode
- 🎚️ Live-adjustable confidence threshold slider
- ⚡ Automatic GPU/CPU device detection
- 🚀 Automatic frame downscaling for high-resolution sources (e.g.,
  portrait/reel-format videos), keeping FPS stable without sacrificing
  detection quality



## Tech Stack

- Python 3.x
- OpenCV — video/image capture, display, drawing, GUI controls
- Ultralytics YOLOv8 — object detection
- ByteTrack (via Ultralytics) — multi-object tracking
- PyTorch — deep learning backend
- NumPy
- Tkinter — native file upload dialogs

## Project Structure

object_detection_tracking/
├── app.py # Main application entry point
├── test_image_detection.py # Standalone detection sanity-check script
├── utils/
│ ├── detector.py # YOLO detection-only wrapper (used for images)
│ ├── tracker.py # YOLO + ByteTrack tracking wrapper, GPU/CPU detection
│ ├── visualization.py # Drawing: boxes, labels, IDs, FPS, counts
│ ├── fps_counter.py # Smoothed FPS calculation
│ ├── video_writer.py # Video output saving
│ ├── object_counter.py # Per-frame and unique object counting
│ ├── ui_controller.py # Keyboard controls and UI state
│ └── input_selector.py # Webcam / video file / image file selection menu
├── models/ # Pretrained YOLO weights
├── videos/ # Sample input videos
├── outputs/ # Saved recordings, screenshots, and image results
├── assets/ # Test images
└── requirements.txt


## Installation

1. Clone the repository:
```bash
   git clone  https://github.com/arunbaskar05/object-detection-tracking.git
   cd object_detection_tracking
```

2. Create and activate a virtual environment:
```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python app.py
```

You'll be prompted to choose an input source:

Select input source:

Webcam
Upload a video file
Upload an image file
Enter 1, 2, or 3:

The pretrained YOLOv8n model downloads automatically on first run if not
already present in `models/`.

### Controls (Webcam / Video File modes)

| Key | Action |
|-----|--------|
| `Q` | Quit the application |
| `R` | Toggle recording on/off |
| `F` | Toggle full-screen mode |
| `S` | Save a screenshot |
| Slider | Adjust detection confidence threshold live |

### Image Mode

Detection runs once on the selected image; the annotated result is
displayed and automatically saved to `outputs/`. Press any key to close
the window.

## How It Works

1. **Input Selection** — The user chooses webcam, video file, or image
   via a console menu; file selections open a native file browser.
2. **Capture** — OpenCV reads frames from the chosen source. High-resolution
   sources (e.g., portrait-format reels) are automatically downscaled to
   a maximum working resolution to keep processing fast without needing
   manual configuration.
3. **Detection** — Each frame is passed through a YOLOv8 model, which
   predicts bounding boxes, class labels, and confidence scores in a
   single forward pass.
4. **Tracking** — For video/webcam input, detected boxes are passed to
   ByteTrack, which uses a Kalman filter for motion prediction and
   IoU-based matching to assign consistent IDs across frames, including
   a second-pass match on low-confidence detections to better handle
   occlusion. Image mode uses detection only, since tracking requires
   multiple frames over time.
5. **Visualization** — Boxes, labels, confidence scores, tracking IDs
   (or class-based colors for images), FPS, and object counts are drawn
   onto each frame.
6. **Output** — The annotated frame is displayed live and saved to a
   video file or image file in `outputs/`.

## Known Limitations

- Detection is limited to the 80 object classes in the COCO dataset;
  objects outside this vocabulary (e.g., a pen, earbuds) will be
  misclassified as the visually closest known class (e.g., a pen may be
  labeled "toothbrush").
- Tracking IDs may change if an object is fully occluded for an extended
  period, moves very quickly between frames, or briefly fails detection
  — this is an inherent characteristic of IoU/motion-based tracking, not
  a bug.
- Full-screen mode behavior can vary slightly across operating systems
  and OpenCV GUI backends.
- CPU inference on very high-resolution video sources may still run
  below real-time speed on lower-end hardware, even with automatic
  downscaling; a GPU is recommended for consistently high FPS.

## Future Improvements

- Line-crossing and region-based counting
- Custom-trained model support for domain-specific objects (e.g., pens,
  earbuds, notebooks)
- Model selection dropdown (nano/small/medium) from the UI
- Deep SORT integration as an alternative tracker option

## Author

Arun baskar V — Built for the CodeAlpha Internship Program