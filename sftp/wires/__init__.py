import pysftp
import os
from log import logger as mylogger
from stat import *


def create_local_folder(folder):
    # 폴더 존재하는지 판단 후 생성
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            mylogger.info("Directory " + folder + " Created ")
        except Exception as e:
            mylogger.error("Directory " + folder +
                           " Created ERROR MSG: " + e)
            return False
    return True


class SSHSession(object):
    # Usage:
    # Detects DSA or RSA from key_file, either as a string filename or a
    # file object.  Password auth is possible, but I will judge you for
    # using it. So:
    # ssh=SSHSession('targetserver.com','root',key_file=open('mykey.pem','r'))
    # ssh=SSHSession('targetserver.com','root',key_file='/home/me/mykey.pem')
    # ssh=SSHSession('targetserver.com','root','mypassword')
    # ssh.put('filename','/remote/file/destination/path')
    # ssh.put_all('/path/to/local/source/dir','/path/to/remote/destination')
    # ssh.get_all('/path/to/remote/source/dir','/path/to/local/destination')
    # ssh.command('echo "Command to execute"')

    def __init__(self, hostname, username, key_file=None, password=None, local_directory=None, remote_directory=None,
                 remote_backup_directory=None):
        #
        #  Accepts a file-like object (anything with a readlines() function)
        #  in either dss_key or rsa_key with a private key.  Since I don't
        #  ever intend to leave a server open to a password auth.
        #
        self.logger = mylogger
        self.local_directory = local_directory
        self.remote_directory = remote_directory
        self.remote_backup_directory = remote_backup_directory

        try:
            self.sftp = pysftp.Connection(host=hostname, username=username, password=password,
                                          default_path=remote_directory)
        except Exception as e:
            self.logger.error(e)

    def sftp_helper(self, sftp, files):
        stats = sftp.listdir_attr('.')
        files[sftp.getcwd()] = [attr.filename for attr in stats if S_ISREG(attr.st_mode)]

        for attr in stats:

            if S_ISDIR(attr.st_mode):  # If the file is a directory, recurse it
                sftp.chdir(attr.filename)
                self.sftp_helper(sftp, files)
                sftp.chdir('..')

    def filelist_recursive(self, target_dir):
        self.sftp.cwd(target_dir)
        files = {}
        self.sftp_helper(self.sftp, files)
        return files

    def get(self, remote, local, filename):

        self.sftp.get(remote + '/' + filename, local + '/' + filename, preserve_mtime=True)

        if os.path.exists(local + '/' + filename):
            self.logger.info(filename + ' IS SAVE SUCCESS')
            self.backup_file(remote, filename)
        else:
            self.logger.error(remote + '/' + filename + 'IS SAVE FAIL')

    def get_all(self, remote_list):

        for folder, files in remote_list:

            # 루트 디렉토리 문자열 제거.
            target_folder = folder.replace(self.remote_directory, '')
            # 폴더구조를 똑같이 복사하기 위한.
            target_folder = self.local_directory + target_folder

            # 폴더 존재하는지 판단 후 생성
            if create_local_folder(folder=target_folder):
                # 파일 모두 가져옴.
                for file in files:
                    remote_file = folder + '/' + file
                    local_file = target_folder + '/' + file

                    # 로컬에 이미 파일이 존재한다면.
                    if os.path.exists(local_file):
                        # 최종 수정시간 비교후 저장.
                        if self.sftp.stat(remote_file).st_mtime > os.stat(local_file).st_mtime:
                            self.get(remote=remote_file, local=local_file)
                    else:
                        self.get(remote=folder, local=target_folder, filename=file)

    def del_file(self, file):
        self.sftp.remove(file)
        self.logger.info(file + ' DELETE')

    def exist_remote_directory(self, remote_directory):
        return self.sftp.exists(remote_directory)

    def backup_file(self, target_directory, target_file):

        child_directory = target_directory.replace(self.remote_directory, '')
        backup_directory = self.remote_directory + '/tmp'

        # custom_make_dir(self.remote_directory + '/tmp', target_directory.replace(self.remote_directory, ''))
        # '/webstore/ns-home/newspaper/work/newswork/news-receiver-agent/data/osen/tmp/img/2020/02/28'

        for child in child_directory.split('/'):
            if child != '':
                backup_directory += '/' + child
                if not self.sftp.exists(backup_directory):
                    self.sftp.mkdir(backup_directory)

        # if not self.sftp.exists(backup_directory):
        #     self.sftp.mkdir(backup_directory)
        print(self.remote_directory + child_directory + '/' + target_file)
        print(backup_directory + '/' + target_file)
        self.sftp.rename(self.remote_directory + child_directory + '/' + target_file,
                         backup_directory + '/' + target_file)

    # def custom_make_dir(self, root, child):
