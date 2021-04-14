import os, time
import yaml

from exif import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import s3fs


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

bucket_a = "images/bucket_a/s3"
bucket_b = "images/bucket_b/s3"


# def open_s3fs_folder():
#    # get aws iam creds
#    with open(os.path.join(ROOT_DIR, ".aws_creds.yml")) as file:
#        aws_creds = yaml.load(file, Loader=yaml.FullLoader)
#    # create instance of s3fs
#    fs = s3fs.S3FileSystem(
#        anon=False,
#        key=aws_creds["key_id"],
#        secret=aws_creds["secret"],
#    )
#    file_list = fs.ls(bucket_a)
#
#    return file_list


def delete_exif_data(new_file: str):
    with open(os.path.join(new_file), "rb") as filea:
        old_image = Image(filea)
        # delete exif metadata
        old_image.delete_all()
    with open(
        os.path.join(ROOT_DIR, bucket_b, os.path.basename(new_file)), "wb"
    ) as fileb:
        # write file in new location
        fileb.write(old_image.get_file())


def main():

    # file_list = open_s3fs_folder()

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