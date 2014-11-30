from time import time
import os
class FileSystemChecker(object):
    def __init__(self, fs):
        self.fs = fs
        self.blocksize = 4096

    def check_dev_id(self, dev_id):
        if self.fs.stats.dev_id == dev_id:
            return True
        else:
            return False

    def check_indirect_size(self):
        if self.fs.stat_ino.indirect== 0 and self.fs.stat.stat_size>0:
            if self.fs.stat.stat_size<self.blocksize:
                return True
            else:
                return False
            return False

        if self.fs.stat_ino.indirect != 0:
            if self.fs.stat.stat_size<self.blocksize*arr.length or self.fs.stat.stat_size>self.blocksize*arr.length-1:
                return True
            else:
                return False
            return False

    def validate_free_block(self):
        System_Free_Block = (self.blocksize) - (self.fs.stats.size)
        if System_Free_Block == os.statvfs(f_bfree):
            return True
        else:
            return False

    def files_in_freeBlock(self):
        freeblocks = (self.blocksize) - (self.fs.stats.size)
        for i in freeblocks:
            if i.fstats.stat_linkcout > 0:
                return True
            else:
                return False

    def check_time(self):
        time_now = time()
        if (self.fs.stats.atime < time_now and self.fs.stats.mtime < time_now and self.fs.stats.ctime < time_now):
            return True
        else:
            return False

    def dir_check(self):
        dir_list = self.fs.readdir("/")
        for i in dir_list:
            if i.stats.nlink < 2:
                return False
        return True

    def link_count(self):
        if (self.fs.nlink == self.fs.inode):
            return True
        else:
            return False


