import json
import os
from stat import *


def json_test():
    with open('/Users/hakgyun/repository_chosunbiz/inbound-script-py/config/config.json', 'r') as f:
        config = json.load(f)

        print(config['osen']['remote_child_path'])

        for children in config['osen']['remote_child_path']:
            print(children)
        # self.env =
        # self.hostname = self.env['server']
        # self.username = self.env['user']
        # self.password = self.env['password']
        # self.local_directory_path = self.env['local_file_path']
        # self.remote_directory_path = self.env['remote_file_path']
        # self.remote_backup_path = self.env['remote_backup_path']


def os_dir_test():
    print(file_list_recursive())


def file_list_helper(self, sftp, files):
    stats = sftp.listdir_attr('.')
    files[sftp.getcwd()] = [attr.filename for attr in stats if S_ISREG(attr.st_mode)]

    for attr in stats:

        if S_ISDIR(attr.st_mode):  # If the file is a directory, recurse it
            sftp.chdir(attr.filename)
            self.sftp_helper(sftp, files)
            sftp.chdir('..')


def file_list_recursive(self):
    files = {}
    file_list_helper(os, files)
    return files


def test():
    test = '<LogRecord: %s, %s, %s, %s, "%s">' % (__file__, __file__,
                                                  __file__, __file__, __file__)

    print('%s DELETE' % test)


if __name__ == '__main__':
    # os.chdir('/Users/hakgyun/repository_chosunbiz/inbound-script-py/get')
    test()
