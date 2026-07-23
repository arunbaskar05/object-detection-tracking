
import time
from collections import deque


class FPSCounter:
    """
    Maintains a rolling window of recent frame timestamps to compute
    a stable, averaged FPS value rather than a jittery instantaneous one.
    """

    def __init__(self, window_size=30):
        """
        window_size: how many recent frames to average over.
                     Larger = smoother but slower to react to real changes.
                     Smaller = more responsive but noisier.
        """
        # deque = a list-like structure optimized for fast add/remove
        # from both ends. maxlen automatically discards the OLDEST
        # timestamp once the window is full — no manual cleanup needed.
        self.timestamps = deque(maxlen=window_size)

    def update(self):
        """
        Call this ONCE per frame. Records the current timestamp and
        returns the current smoothed FPS based on the rolling window.
        """
        self.timestamps.append(time.time())

        # Need at least 2 timestamps to calculate any elapsed time
        if len(self.timestamps) < 2:
            return 0.0

        # Time elapsed between the OLDEST and NEWEST timestamps in our window
        elapsed = self.timestamps[-1] - self.timestamps[0]

        if elapsed == 0:
            return 0.0

        # FPS = (number of frames in window - 1) / (time elapsed)
        # We use (len - 1) because N timestamps only span (N-1) intervals
        fps = (len(self.timestamps) - 1) / elapsed
        return fps