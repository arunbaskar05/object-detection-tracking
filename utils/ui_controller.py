

import cv2
import os
from datetime import datetime


class UIController:
    

    # Default window size when NOT in fullscreen mode. Chosen to be
    # comfortably smaller than most screens, regardless of the actual
    # webcam/video capture resolution.
    DEFAULT_WIDTH = 960
    DEFAULT_HEIGHT = 540

    def __init__(self, window_name, screenshot_dir="outputs"):
        self.window_name = window_name
        self.screenshot_dir = screenshot_dir
        os.makedirs(screenshot_dir, exist_ok=True)

        self.is_recording = True
        self.is_fullscreen = False

        # IMPORTANT FIX: explicitly force the window to a sane default
        # size immediately on startup. Without this, the window inherits
        # a size based on the raw frame resolution, which can appear
        # "fullscreen-like" even though it isn't actually in fullscreen
        # mode — this is exactly why 'f' previously seemed to do nothing.
        cv2.resizeWindow(self.window_name, self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)

    def handle_key(self, key):
        
        if key == ord('q'):
            return True

        elif key == ord('r'):
            self.is_recording = not self.is_recording
            state = "ON" if self.is_recording else "OFF"
            print(f"Recording: {state}")

        elif key == ord('f'):
            self.is_fullscreen = not self.is_fullscreen
            self._apply_fullscreen()

        return False

    def _apply_fullscreen(self):
        
        if self.is_fullscreen:
            cv2.setWindowProperty(
                self.window_name,
                cv2.WND_PROP_FULLSCREEN,
                cv2.WINDOW_FULLSCREEN
            )
        else:
            cv2.setWindowProperty(
                self.window_name,
                cv2.WND_PROP_FULLSCREEN,
                cv2.WINDOW_NORMAL
            )
            # Re-apply our sane default size when returning to normal mode,
            # since just clearing the fullscreen flag alone can leave the
            # window stuck at whatever size it was before (which, without
            # this, would just go back to the oversized default).
            cv2.resizeWindow(
                self.window_name, self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT
            )

    def take_screenshot(self, frame):
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.jpg")
        cv2.imwrite(path, frame)
        print(f"Screenshot saved: {path}")