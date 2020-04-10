import logging
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from wires.client import S3Client


class LocalJob:
    # DIRECTORY_TO_WATCH = "/Users/hakgyun/repository_chosunbiz/inbound-script-py/get"

    def __init__(self, env, config, name):
        self.logger = logging.getLogger("%s_%s" % (name, self.__class__.__qualname__))
        self.observer = Observer()
        self.env = env
        self.local_obj = config
        self.directory = self.local_obj['local_file_path']

    def run(self):
        event_handler = LocalJobHandler(env=self.env, config=self.local_obj)
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            self.logger.error("Error" + e)

        self.observer.join()


class LocalJobHandler(FileSystemEventHandler):

    def __init__(self, env, config):
        self.local_obj = config
        self.logger = logging.getLogger("%s_%s" % (self.local_obj['name'], self.__class__.__qualname__))
        self.aws_obj = env['AWS']
        self.bucket_name = "%s-%s" % (self.local_obj['name'], self.aws_obj['BUCKET_NAME'])

        self.s3_client = S3Client(aws_access_key_id=self.aws_obj['AWS_ACCESS_KEY_ID'],
                                  aws_secret_access_key=self.aws_obj['AWS_SECRET_ACCESS_KEY'],
                                  region_name=self.aws_obj['REGION_NAME'])

    def on_any_event(self, event):

        key = 'photo/' + os.path.basename(event.src_path)

        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            self.logger.info("Received created event - %s." % event.src_path)
            self.logger.info("Received created event - %s." % os.path.basename(event.src_path))

            self.s3_client.file_upload(bucket_name=self.bucket_name, file_path=event.src_path,
                                       file_key=key)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            self.logger.info("Received modified event - %s." % event.src_path)
            self.logger.info("Received created event - %s." % os.path.basename(event.src_path))

            self.s3_client.file_upload(bucket_name=self.bucket_name, file_path=event.src_path,
                                       file_key=key)
