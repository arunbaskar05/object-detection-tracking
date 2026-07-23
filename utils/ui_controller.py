
import cv2
import os
from datetime import datetime


class UIController:
    

    def __init__(self, window_name, screenshot_dir="outputs"):
        self.window_name = window_name
        self.screenshot_dir = screenshot_dir
        os.makedirs(screenshot_dir, exist_ok=True)

        # Interactive state flags — start with recording ON and
        # fullscreen OFF as sensible defaults.
        self.is_recording = True
        self.is_fullscreen = False

    def handle_key(self, key):
        
        if key == ord('q'):
            return True  # Signal to app.py: time to exit the main loop

        elif key == ord('r'):
            # Toggle recording on/off
            self.is_recording = not self.is_recording
            state = "ON" if self.is_recording else "OFF"
            print(f"Recording: {state}")

        elif key == ord('f'):
            # Toggle fullscreen on/off
            self.is_fullscreen = not self.is_fullscreen
            self._apply_fullscreen()

        elif key == ord('s'):
            # Screenshot is handled separately since it needs the actual
            # frame data, not just a state flip — see take_screenshot()
            pass  # app.py will call take_screenshot() directly for 's'

        return False  # Don't quit

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
            cv2.resizeWindow(self.window_name, 960, 720)
    def take_screenshot(self, frame):
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.jpg")
        cv2.imwrite(path, frame)
        print(f"Screenshot saved: {path}")