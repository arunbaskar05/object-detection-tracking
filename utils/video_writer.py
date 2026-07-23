
import cv2
import os
from datetime import datetime


class VideoWriter:
   
    def __init__(self, output_dir="outputs", frame_width=640, frame_height=480, fps=20):
        
        # Ensure the output directory exists; create it if not.
        # exist_ok=True prevents an error if the folder already exists.
        os.makedirs(output_dir, exist_ok=True)

        # Generate a unique filename using the current timestamp,
        # so re-running the app never overwrites a previous recording.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"output_{timestamp}.mp4")

        # FourCC codec identifier for mp4 output
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        # Initialize the actual OpenCV VideoWriter object
        self.writer = cv2.VideoWriter(
            output_path, fourcc, fps, (frame_width, frame_height)
        )

        self.output_path = output_path
        print(f"Recording will be saved to: {self.output_path}")

    def write(self, frame):
        
        self.writer.write(frame)

    def release(self):
        
        self.writer.release()