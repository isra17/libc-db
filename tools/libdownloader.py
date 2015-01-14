import urllib
import tempfile
import os
import shutil
import binascii
from subprocess import call
from tools.chdir import ChDir
from os import path, urandom

class LibDownloader:
    def __init__(self, target):
        self.target = target
        self.filename = path.basename(target)
        self.workdir = path.join(tempfile.gettempdir(), path.splitext(self.filename)[0])
        self.target_location = path.join(self.workdir, self.filename)
        self.location = path.join(tempfile.gettempdir(), binascii.hexlify(urandom(16)).decode())

        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

        self.download()
        self.extract()
        self.clean()

    def download(self):
        urllib.request.urlretrieve(self.target, self.target_location)

    def extract(self):
        with ChDir(self.workdir):
            ext = path.splitext(self.filename)[1]
            if ext == '.deb':
                call(['ar', 'xv', self.target_location])
                call(['tar', 'zxvf', 'data.tar.gz', '.'])

                for dirpath, dirs, files in os.walk(path.join(self.workdir, 'lib')):
                    if 'libc.so.6' in files:
                        libc_location = path.join(dirpath, 'libc.so.6')

        shutil.copy(libc_location, self.location)
        print('* libc extracted to {}'.format(self.location))

    def clean(self):
        shutil.rmtree(self.workdir)
