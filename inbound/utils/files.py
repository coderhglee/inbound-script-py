import logging
import math
import os

logger = logging.getLogger(__name__)


def create_local_folder(folder):
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


#  오차범위 감안하며 수정 밀리세컨즈는 100 나누고 나머지값은 절삭한다.
def ms_turc(time):
    return math.trunc(time / 10.0)
