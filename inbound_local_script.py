import logging

from watchdog.events import FileSystemEventHandler

from inbound import Watcher


# class Watcher:
#     DIRECTORY_TO_WATCH = "/Users/hakgyun/repository_chosunbiz/inbound-script-py/get"
#
#     def __init__(self):
#         self.observer = Observer()
#
#     def run(self):
#         event_handler = Handler()
#         self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
#         self.observer.start()
#         try:
#             while True:
#                 time.sleep(5)
#         except Exception as e:
#             self.observer.stop()
#             print("Error"+e)
#
#         self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self):
        self.logger = logging.getLogger("%s" % self.__class__.__qualname__)

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)


if __name__ == '__main__':
    w = Watcher(directory="/Users/hakgyun/repository_chosunbiz/inbound-script-py/get", handler=Handler())
    w.run()
