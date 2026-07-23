
import cv2
import random


_id_colors = {}

# --- Centralized text styling constants ---
# Tweak these here if text still looks too small/large on your screen.
FONT = cv2.FONT_HERSHEY_SIMPLEX
BOX_LABEL_FONT_SCALE = 0.7
BOX_LABEL_THICKNESS = 2
FPS_FONT_SCALE = 1.1
FPS_THICKNESS = 3
COUNTS_FONT_SCALE = 0.8
COUNTS_THICKNESS = 2


def _get_color(track_id, class_id):
    key = f"track_{track_id}" if track_id is not None else f"class_{class_id}"

    if key not in _id_colors:
        random.seed(key)
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )
        _id_colors[key] = color

    return _id_colors[key]


def draw_detections(frame, results):
    
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = results.names[class_id]

        if box.id is not None:
            track_id = int(box.id[0])
            color = _get_color(track_id, class_id)
            label = f"ID:{track_id} {class_name} {confidence:.2f}"
        else:
            color = _get_color(None, class_id)
            label = f"{class_name} {confidence:.2f}"

        # Bounding box outline — slightly thicker too, for visibility
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

        (text_width, text_height), baseline = cv2.getTextSize(
            label, FONT, BOX_LABEL_FONT_SCALE, BOX_LABEL_THICKNESS
        )
        cv2.rectangle(
            frame,
            (x1, y1 - text_height - baseline - 8),
            (x1 + text_width + 4, y1),
            color,
            -1
        )
        cv2.putText(
            frame, label, (x1 + 2, y1 - 6),
            FONT, BOX_LABEL_FONT_SCALE, (0, 0, 0), BOX_LABEL_THICKNESS
        )

    return frame


def draw_fps(frame, fps):
    
    text = f"FPS: {fps:.1f}"
    cv2.putText(
        frame, text, (15, 40),
        FONT, FPS_FONT_SCALE, (0, 0, 255), FPS_THICKNESS
    )
    return frame


def draw_counts(frame, per_frame_counts, unique_total_count, start_y=85):
    
    y = start_y

    cv2.putText(
        frame, f"Unique Objects Tracked: {unique_total_count}",
        (15, y), FONT, COUNTS_FONT_SCALE, (255, 255, 0), COUNTS_THICKNESS
    )
    y += 35

    for class_name, count in per_frame_counts.items():
        cv2.putText(
            frame, f"{class_name}: {count}",
            (15, y), FONT, COUNTS_FONT_SCALE - 0.1, (255, 255, 255), 2
        )
        y += 28

    return frame