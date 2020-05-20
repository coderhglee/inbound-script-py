import logging
from stat import *
import pysftp
from inbound.utils import files as fileUtils


class SftpSession(object):

    def __init__(self, hostname, username, key_file=None, password=None, local_directory=None, remote_directory=None,
                 remote_backup_directory=None):
        """

        :param hostname:
        :param username:
        :param key_file:
        :param password:
        :param local_directory:
        :param remote_directory:
        :param remote_backup_directory:
        """
        self.local_directory = local_directory
        self.remote_directory = remote_directory
        self.remote_backup_directory = remote_backup_directory

        self.logger = logging.getLogger("%s" % self.__class__.__qualname__)

        try:
            self.sftp = pysftp.Connection(host=hostname, username=username, password=password,
                                          default_path=remote_directory)
        except Exception as e:
            self.logger.error(e)

    def file_list_helper(self, sftp, files):
        """

        :param sftp:
        :param files:
        :return:
        """
        stats = sftp.listdir_attr('.')
        files[sftp.getcwd()] = [attr.filename for attr in stats if S_ISREG(attr.st_mode)]

        for attr in stats:

            if S_ISDIR(attr.st_mode):  # If the file is a directory, recurse it
                sftp.chdir(attr.filename)
                self.sftp_helper(sftp, files)
                sftp.chdir('..')

    def file_list_recursive(self):
        """

        :return:
        """
        files = {}
        self.file_list_helper(self.sftp, files)
        return files

    def get(self, remote, local, filename):
        """

        :param remote:
        :param local:
        :param filename:
        :return:
        """
        self.sftp.get("%s/%s" % (remote, filename), "%s/%s" % (local, filename), preserve_mtime=True)

        if fileUtils.exist_local_file("%s/%s" % (local, filename)):
            self.logger.info('%s IS SAVE SUCCESS' % filename)
            self.backup_file(remote, filename)
        else:
            self.logger.error('%s/%s IS SAVE FAIL' % (remote, filename))

    def get_all(self, remote_list):
        """

        :param remote_list:
        :return:
        """
        for folder, files in remote_list:

            self.logger.info("Get All Files, remote Directory files size: " + str(len(files)))
            # 폴더구조를 똑같이 복사하기 위한.
            # 루트 디렉토리 문자열 제거.
            target_folder = self.local_directory + folder.replace(self.remote_directory, '')
            # target_folder = self.local_directory + target_folder

            # 폴더 존재하는지 판단 후 생성
            if fileUtils.create_local_folder(folder=target_folder):
                # 파일 모두 가져옴.
                for file in files:
                    remote_file = '%s/%s' % (folder, file)
                    local_file = '%s/%s' % (target_folder, file)

                    # 로컬에 이미 파일이 존재한다면.
                    if fileUtils.exist_local_file(local_file):
                        # 최종 수정시간 비교후 저장.
                        remote_file_time = fileUtils.ms_turc(self.sftp.stat(remote_file).st_mtime)
                        local_file_time = fileUtils.ms_turc(fileUtils.get_stat_file(local_file).st_mtime)

                        if remote_file_time > local_file_time:
                            self.get(remote=folder, local=target_folder, filename=file)
                        else:
                            self.logger.info('%s is Not modified' % file)
                    else:
                        self.get(remote=folder, local=target_folder, filename=file)

    def del_file(self, file):
        self.sftp.remove(file)
        self.logger.info('%s DELETE' % file)

    def exist_remote_directory(self, remote_directory):
        return self.sftp.exists(remote_directory)

    def backup_file(self, target_directory, target_file):
        """

        :param target_directory:
        :param target_file:
        :return:
        """
        child_directory = target_directory.replace(self.remote_directory, '')
        backup_directory = self.remote_backup_directory

        # custom_make_dir(self.remote_directory + '/tmp', target_directory.replace(self.remote_directory, ''))
        # '/webstore/ns-home/newspaper/work/newswork/news-receiver-agent/data/osen/tmp/img/2020/02/28'

        for child in child_directory.split('/'):
            if child != '':
                backup_directory += '/' + child
                if not self.sftp.exists(backup_directory):
                    self.sftp.mkdir(backup_directory)

        # if not self.sftp.exists(backup_directory):
        #     self.sftp.mkdir(backup_directory)
        # print(self.remote_directory + child_directory + '/' + target_file)
        # print(backup_directory + '/' + target_file)

        remote_full_path = '%s%s/%s' % (self.remote_directory, child_directory, target_file)
        backup_full_path = '%s/%s' % (backup_directory, target_file)
        if self.exist_remote_directory(backup_full_path):
            self.sftp.remove(backup_full_path)
            self.sftp.rename(remote_full_path, backup_full_path)
        else:
            self.sftp.rename(remote_full_path, backup_full_path)
