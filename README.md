# Real-Time Object Detection and Tracking System

A real-time computer vision system that detects and tracks multiple objects
from a live webcam feed or video file, using YOLOv8 for detection and
ByteTrack for multi-object tracking. Built as part of the CodeAlpha
internship program.

## Features

- 🎥 Live webcam and video file input
- 🎯 Real-time object detection using YOLOv8 (COCO 80-class pretrained)
- 🆔 Persistent multi-object tracking with unique IDs (ByteTrack)
- 🎨 Unique color per tracked object for easy visual distinction
- 📊 Live FPS counter (smoothed rolling average)
- 🔢 Per-frame and unique (session-total) object counting, per class
- 💾 Save annotated video output automatically
- 📸 On-demand screenshot capture
- ⏺️ Toggleable recording (start/stop without restarting the app)
- 🖥️ Full-screen display mode
- 🎚️ Live-adjustable confidence threshold slider
- ⚡ Automatic GPU/CPU device detection



## Tech Stack

- Python 3.x
- OpenCV — video capture, display, drawing, GUI controls
- Ultralytics YOLOv8 — object detection
- ByteTrack (via Ultralytics) — multi-object tracking
- PyTorch — deep learning backend
- NumPy

## Project Structure

\`\`\`
object_detection_tracking/
├── app.py                  # Main application entry point
├── utils/
│   ├── detector.py          # YOLO detection wrapper
│   ├── tracker.py           # YOLO + ByteTrack tracking wrapper
│   ├── visualization.py     # Drawing: boxes, labels, IDs, FPS, counts
│   ├── fps_counter.py       # Smoothed FPS calculation
│   ├── video_writer.py      # Video output saving
│   ├── object_counter.py    # Per-frame and unique object counting
│   └── ui_controller.py     # Keyboard controls and UI state
├── models/                  # Pretrained YOLO weights
├── videos/                  # Sample input videos
├── outputs/                 # Saved recordings and screenshots
├── assets/                  # Test images
└── requirements.txt
\`\`\`

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone <https://github.com/arunbaskar05/object-detection-tracking.git>
   cd object_detection_tracking
   \`\`\`

2. Create and activate a virtual environment:
   \`\`\`bash
   python -m venv venv
   # Windows:
   venv\\Scripts\\activate
   # macOS/Linux:
   source venv/bin/activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Usage

Run the application:
\`\`\`bash
python app.py
\`\`\`

The pretrained YOLOv8n model downloads automatically on first run if not
already present in \`models/\`.

### Controls

| Key | Action |
|-----|--------|
| `Q` | Quit the application |
| `R` | Toggle recording on/off |
| `F` | Toggle full-screen mode |
| `S` | Save a screenshot |
| Slider | Adjust detection confidence threshold live |

## How It Works

1. **Capture** — OpenCV reads frames from the webcam/video source.
2. **Detection** — Each frame is passed through a YOLOv8 model, which
   predicts bounding boxes, class labels, and confidence scores in a
   single forward pass.
3. **Tracking** — Detected boxes are passed to ByteTrack, which uses a
   Kalman filter for motion prediction and IoU-based matching to assign
   consistent IDs across frames, including a second-pass match on
   low-confidence detections to better handle occlusion.
4. **Visualization** — Boxes, labels, confidence scores, tracking IDs,
   FPS, and object counts are drawn onto each frame.
5. **Output** — The annotated frame is displayed live and optionally
   saved to a video file.

## Known Limitations

- Detection is limited to the 80 object classes in the COCO dataset;
  objects outside this vocabulary (e.g., a pen, earbuds) will be
  misclassified as the visually closest known class.
- Tracking IDs may change if an object is fully occluded for an extended
  period, moves very quickly between frames, or briefly fails detection
  — this is an inherent characteristic of IoU/motion-based tracking, not
  a bug.
- Full-screen mode behavior can vary slightly across operating systems
  and OpenCV GUI backends.

## Future Improvements

- Line-crossing and region-based counting
- Custom-trained model support for domain-specific objects
- Model selection dropdown (nano/small/medium) from the UI
- Deep SORT integration as an alternative tracker option

## Author

Arun baskar V — Built for the CodeAlpha Internship Program