
class ObjectCounter:


    def __init__(self):
        # A set (not a list!) storing every unique track ID we've ever seen.
        # Sets automatically prevent duplicates — adding the same ID twice
        # has no effect, which is exactly the behavior we want here.
        self._seen_ids = set()

        # Maps class_name -> set of unique track IDs seen for that class
        # e.g., {"person": {1, 4, 7}, "laptop": {2}}
        self._seen_ids_per_class = {}

    def update(self, results):
        
        # --- Per-frame counting (resets every call, no memory needed) ---
        per_frame_counts = {}

        for box in results.boxes:
            class_id = int(box.cls[0])
            class_name = results.names[class_id]

            # .get(class_name, 0) + 1 -> if class_name isn't in the dict yet,
            # default to 0, then add 1. This is a common Python counting idiom.
            per_frame_counts[class_name] = per_frame_counts.get(class_name, 0) + 1

            # --- Unique counting (persists across frames) ---
            # Only count toward the "unique ever seen" total if this box
            # actually has a track ID assigned (guards against the brief
            # None case discussed in Step 5).
            if box.id is not None:
                track_id = int(box.id[0])

                # Add to our overall set of every ID ever seen
                self._seen_ids.add(track_id)

                # Add to the per-class set too, creating it if it's new
                if class_name not in self._seen_ids_per_class:
                    self._seen_ids_per_class[class_name] = set()
                self._seen_ids_per_class[class_name].add(track_id)

        unique_total_count = len(self._seen_ids)

        # Convert each class's SET into just its COUNT (a number),
        # since that's what we actually want to display.
        unique_counts_per_class = {
            class_name: len(ids)
            for class_name, ids in self._seen_ids_per_class.items()
        }

        return per_frame_counts, unique_total_count, unique_counts_per_class