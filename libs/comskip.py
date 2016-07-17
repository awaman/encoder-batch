from libs.config import Config
from libs.decorator import lockfile_manager
from libs.common import Base, copy_timestamp
from libs import chinachu

config = Config().comskip
lock_file = config['lock_file']
client = chinachu.client()


def comskip_execute(filename):
    if client.recording.is_busy():
        raise RuntimeError('Recording now')
    comskip = ComskipBatchWrapper()
    comskip.execute(filename)


class ComskipBatchWrapper(Base):

    def __init__(self):
        self.cmd = config['cmd']
        self.dest_dir = config['dest_dir']
        self.backup_dir = config['backup_dir']

    @lockfile_manager(lock_file)
    def execute(self, filename):
        cmd_opt = self._create_cmd_opt({
                'margin': '3', 'file': filename,
                'move_to': self.dest_dir, 'failed_to': self.backup_dir})
        self._execute_cmd(self.cmd, cmd_opt)
        copy_timestamp(filename, afterdir=self.dest_dir)
