#!/usr/bin/env python


#Name  - Abhishek Rai
#Net id  - ar3859
#NID: N12456232

#Resources -
#SourceForge: http://sourceforge.net/apps/mediawiki/fuse/index.php?title=FUSE_Python_Reference
#MIT: http://stuff.mit.edu/iap/2009/fuse/examples/xmp.py

import errno
import fuse
import stat
import sys
from collections import defaultdict
from fuse import Fuse, Stat
from time import time

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "fuse.__version__ unknown,fuse-py too old."

fuse.fuse_python_api = (0, 2)

class Statistics(Stat):
    """ Class representing stats. """
    def __init__(self):
        time_now = time()
        self.mode = 0
        self.inode = 0
        self.dev_id = 0
        self.nlink = 0
        self.uid = 0
        self.gid = 0
        self.size = 0
        self.atime = time_now
        self.mtime = time_now
        self.ctime = time_now


class FileSystem(Fuse):
    """ Current only single level file system supported """

    def __init__(self):
        self.files = {}
        self.contents = defaultdict(str)    # Empty String
        self.openCount = 0
        stats = Statistics()
        stats.mode   = stat.S_IFDIR | 0755
        stats.nlink  = 2                 # Every directory has . and ..
        stats.size   = 4096              # The size of an empty directory
        self.files['/'] =  stats


    def readlink(self, path):
        return self.contents[path]

    def mknod(self, path, mode, dev):
        stats = Statistics()
        self.files[path] = stats
        return 0

    def mkdir(self, path, mode):
        time_now = time()
        stats = Statistics()
        stats.mode   = stat.S_IFDIR | mode
        stats.nlink  = 2
        stats.size   = 4096

        self.files[path] = stats
        self.files['/'].nlink += 1

    def unlink(self, path):
        self.files.pop(path)

    def symlink(self, target, name):
        stats = Statistics()
        stats.mode   = stat.S_IFLNK | 0777
        stats.nlink  = 1
        stats.size   = len(name)

        self.files[target] = stats
        self.contents[target] = name

    def rename(self, old, new):
        oldStats = self.files.pop(old)
        self.files[new] = oldStats      # Old File Stats

    def open(self, path, flags):
        self.openCount += 1
        return self.openCount

    def create(self, path, flags, mode):
        now = time()
        stats = Statistics()
        stats.mode   = stat.S_IFREG | mode
        stats.nlink  = 1

        self.files[path] = stats
        self.openCount += 1     # File Opened when created
        return self.openCount

    def read(self, path, size, offset, fh):
        return self.contents[path][offset:offset + size]

    def readdir(self, path, fh):
        direntries = ['.', '..'] + [f[1:] for f in self.files if f != '/']
        for entry in direntries:
            yield fuse.Direntry(entry)

    def write(self, path, data, offset, fh):
        self.contents[path] = self.contents[path][:offset] + data
        self.files[path].size = len(self.contents[path])
        return len(data)

    def getattr(self, path, fh=None):
        if path not in self.files:
            return -errno.ENOENT

        return self.files[path]

    def chmod(self, path, mode):
        return 0

    def chown(self, path, uid, gid):
        self.files[path].uid = uid
        self.files[path].gid = gid

    def rmdir(self, path):
        self.files.pop(path)
        self.files['/'].nlink -= 1

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def truncate(self, path, length, fh=None):
        self.contents[path] = self.contents[path][:length]
        self.files[path].size = length

    def utime(self, path, times):
        time_now = time()
        atime, mtime = times if times else (time_now, time_now)
        self.files[path].atime = atime
        self.files[path].mtime = mtime


def main():
    fs = FileSystem()
    fs.multithreaded = 0
    fs.main(sys.argv)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: %s <mountpoint>' % sys.argv)
        sys.exit(1)
    main()