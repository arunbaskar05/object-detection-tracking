"""
input_selector.py
Lets the user choose: webcam, a video file, or a single image file.
"""

import os
import tkinter as tk
from tkinter import filedialog

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")
VIDEO_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv")


def choose_video_source():
    """
    Prompts the user to choose an input source.

    returns: a tuple (source, source_type)
        source: 0 (webcam) OR a file path (string)
        source_type: "webcam", "video", or "image"
    """
    print("\nSelect input source:")
    print("  1. Webcam")
    print("  2. Upload a video file")
    print("  3. Upload an image file")

    choice = input("Enter 1, 2, or 3: ").strip()

    if choice in ("2", "3"):
        root = tk.Tk()
        root.withdraw()

        if choice == "2":
            file_path = filedialog.askopenfilename(
                title="Select a video file",
                filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
            )
        else:
            file_path = filedialog.askopenfilename(
                title="Select an image file",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
            )

        root.destroy()

        if not file_path:
            print("No file selected. Falling back to webcam.")
            return 0, "webcam"

        # Determine actual type from the extension, rather than trusting
        # the menu choice blindly — protects against a user picking an
        # image while in the "video" dialog's "All files" filter, etc.
        ext = os.path.splitext(file_path)[1].lower()

        if ext in IMAGE_EXTENSIONS:
            print(f"Selected image file: {file_path}")
            return file_path, "image"
        elif ext in VIDEO_EXTENSIONS:
            print(f"Selected video file: {file_path}")
            return file_path, "video"
        else:
            print(f"Unrecognized file type '{ext}'. Falling back to webcam.")
            return 0, "webcam"

    print("Using webcam.")
    return 0, "webcam"