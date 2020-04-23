import logging
import os
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from wires.client import S3Client


class LocalJob:

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
                # print('polling')
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            self.logger.error("Error" + e)

        self.observer.join()


class LocalJobHandler(PatternMatchingEventHandler):

    def __init__(self, env, config):
        # PatternMatchingEventHandler __init__
        super().__init__(patterns=config['file_patterns'], ignore_patterns=[],
                         ignore_directories=True)
        self.local_obj = config
        self.logger = logging.getLogger("%s_%s" % (self.local_obj['name'], self.__class__.__qualname__))
        self.aws_obj = env['AWS']
        self.bucket_name = "%s-%s" % (self.local_obj['name'], self.aws_obj['BUCKET_NAME'])

        self.s3_client = S3Client(aws_access_key_id=self.aws_obj['AWS_ACCESS_KEY_ID'],
                                  aws_secret_access_key=self.aws_obj['AWS_SECRET_ACCESS_KEY'],
                                  region_name=self.aws_obj['REGION_NAME'])

    def on_any_event(self, event):

        key = "%s/%s" % (self.local_obj['s3_key'], os.path.basename(event.src_path))

        if event.is_directory:
            return None

        event_file_path = event.src_path
        event_file_name = os.path.basename(event.src_path)

        if event.event_type == 'created':
            # Take any action here when a file is first created.
            self.logger.info("Received created event - %s." % event_file_name)
            self.logger.info("Received created event - %s." % event_file_path)

            self.s3_client.file_upload(bucket_name=self.bucket_name, file_path=event.src_path,
                                       file_key=key)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            self.logger.info("Received modified event - %s." % event_file_name)
            self.logger.info("Received modified event - %s." % event_file_path)

            self.s3_client.file_upload(bucket_name=self.bucket_name, file_path=event.src_path,
                                       file_key=key)

        if os.path.exists(event_file_path):
            self.logger.info("Remove local file - %s." % event_file_path)
            os.remove(event_file_path)
