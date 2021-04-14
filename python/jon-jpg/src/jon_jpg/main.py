import os, time, io
from io import BytesIO
import yaml

from exif import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import s3fs


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

bucket_a = "images/bucket_a/s3"
bucket_b = "images/bucket_b/s3"
tmp = "images/tmp"


def delete_exif_data(new_file: str):
    # hack to fix the 0kb issue - needs sorting
    time.sleep(5)
    with open(os.path.join(new_file), "rb") as filea:

        old_image = Image(filea)

        if old_image.has_exif:
            old_image.delete_all()

    ## save in s3 bucket B
    with open(
        os.path.join(ROOT_DIR, bucket_b, os.path.basename(new_file)), "wb"
    ) as fileb:
        # fileb.seek(0)
        # write file in new location
        fileb.write(old_image.get_file())


def main():

    w = Watcher()
    w.run()


class Watcher:

    WATCH_PATH = os.path.join(ROOT_DIR, bucket_a)

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.WATCH_PATH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == "created":
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            delete_exif_data(event.src_path)

        elif event.event_type == "modified":
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)
            # delete_exif_data(event.src_path)


if __name__ == "__main__":
    main()