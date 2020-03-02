import os
import logging


def create_local_folder(folder):

    logger = logging.getLogger('myLogger')
    # 폴더 존재하는지 판단 후 생성
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            logger.info("Directory " + folder + " Created ")
        except Exception as e:
            logger.error("Directory " + folder +
                           " Created ERROR MSG: " + e)
            return False
    return True


def exist_local_file(local_file_path):
    return os.path.exists(local_file_path)


def get_stat_file(local_file_path):
    return os.stat(local_file_path)
