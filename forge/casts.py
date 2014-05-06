import os
import tempfile

class Cast(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def clone(self, directory):
        cloned_cast = self._create_cloned_cast()
        if cloned_cast is not None:
            cloned_cast.process_choices()
            cloned_cast.copy_files()

    def _create_cloned_cast(self):
        if self.type == "zip":
            return ZipClonedCast(self.url)
        elif self.type == 'git':
            return GitClonedCast(self.url)
        elif self.type == 'hg':
            return HgClonedCast(self.url)
        else:
            return None


class ClonedCast(object):
    def __init__(self, location):
        self.location = location
        self.temp_dir = tempfile.mkdtemp()
        self.do_clone()

    def do_clone(self):
        pass

    def copy_files(self):
        pass

    def process_choices(self):
        pass

class ZipClonedCast(ClonedCast):
    pass

class GitClonedCast(ClonedCast):
    def do_clone(self):
        os.system("git clone %s %s" % (self.location, self.temp_dir))


class HgClonedCast(ClonedCast):
    def do_clone(self):
        os.system("hg clone %s %s" % (self.location, self.temp_dir))
