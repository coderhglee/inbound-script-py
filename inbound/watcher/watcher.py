import logging
import time

from watchdog.observers import Observer


class Watcher:

    def __init__(self, directory, handler):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory
        self.logger = logging.getLogger("%s" % self.__class__.__qualname__)

    def run(self):
        # event_handler = Handler()
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()
        self.logger.info("Watcher Start")
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()

            self.logger.info(e)
            self.logger.info("Watcher Stop")

        self.observer.join()
