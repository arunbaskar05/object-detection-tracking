
import cv2
import random


# This dictionary persists across function calls because it's defined
# at MODULE level (not inside the function) — it lives as long as the
# program runs, acting as our "memory" of which color belongs to which ID.
_id_colors = {}


def _get_color_for_id(track_id):
    
    if track_id not in _id_colors:
        # Generate a random color (B, G, R) each between 0-255.
        # random.seed(track_id) ensures reproducibility: the SAME id
        # will always generate the SAME "random" color, even across
        # different runs of the program — useful for consistent demos.
        random.seed(track_id)
        color = (
            random.randint(50, 255),  # Blue channel (avoid too-dark colors)
            random.randint(50, 255),  # Green channel
            random.randint(50, 255),  # Red channel
        )
        _id_colors[track_id] = color

    return _id_colors[track_id]


def draw_detections(frame, results):
    
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = results.names[class_id]

        # box.id is None if tracking hasn't assigned an ID yet
        # (can briefly happen on the very first frame an object appears).
        # We guard against this with a fallback label.
        if box.id is not None:
            track_id = int(box.id[0])
            color = _get_color_for_id(track_id)
            label = f"ID:{track_id} {class_name} {confidence:.2f}"
        else:
            track_id = None
            color = (0, 255, 0)  # Default green if no ID yet
            label = f"{class_name} {confidence:.2f}"

        # Draw bounding box using this object's unique color
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Draw label background + text (same approach as before)
        (text_width, text_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        )
        cv2.rectangle(
            frame,
            (x1, y1 - text_height - 10),
            (x1 + text_width, y1),
            color,
            -1
        )
        cv2.putText(
            frame, label, (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1
        )

    return frame


def draw_fps(frame, fps):
    
    text = f"FPS: {fps:.1f}"
    cv2.putText(
        frame, text, (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
    )
    return frame

def draw_counts(frame, per_frame_counts, unique_total_count, start_y=70):

    y = start_y

    # Draw the running unique total first — this is the "headline" number
    cv2.putText(
        frame, f"Unique Objects Tracked: {unique_total_count}",
        (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2
    )
    y += 25

    # Draw per-frame breakdown, one line per class
    for class_name, count in per_frame_counts.items():
        cv2.putText(
            frame, f"{class_name}: {count}",
            (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
        )
        y += 20  # Move down for the next line

    return frame