import json
import logging
import os
from StringIO import StringIO
import zipfile
from jinja2 import Template
import requests
import tempfile
import shutil


class Cast(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.type = None
        self.url = ''
        self.__dict__.update(kwargs)

    def clone(self, directory):
        cloned_cast = self._create_cloned_cast(directory)
        if cloned_cast is not None:
            cloned_cast.process_choices()
            cloned_cast.copy_files()
            cloned_cast.apply_jinja()

    def _create_cloned_cast(self, directory):
        if self.type == "zip":
            return ZipClonedCast(self.url, directory)
        elif self.type == 'git':
            return GitClonedCast(self.url, directory)
        elif self.type == 'hg':
            return HgClonedCast(self.url, directory)
        else:
            return None


class ClonedCast(object):
    def __init__(self, location, directory):
        self.context = {}
        self.location = location
        self.directory = directory
        self.temp_dir = tempfile.mkdtemp()
        self.cast_root = self.temp_dir

        self.do_clone()

    def do_clone(self):
        pass

    def copy_files(self):
        shutil.copytree(self.cast_root, self.directory)

    def process_choices(self):
        self.cast_root, choices_path = self._find_choices()
        if choices_path is not None:
            with open(choices_path) as choices_file:
                try:
                    choices = json.load(choices_file)
                except ValueError, e:
                    logging.error("Invalid json in the projects forger.json: %s", e.message)
                    return

                for c in choices:
                    if 'choices' in c.keys():
                        answer = None
                        while answer not in c['choices']:
                            answer = raw_input("%s [%s] >>> " % (c['question'], ",".join(c['choices'])))
                    else:
                        answer = raw_input(c['question'] + " >>> ")
                    self.context[c['name']] = answer

    def apply_jinja(self):
        for path, dirs, files in os.walk(self.directory):
            for jinja_file in [f for f in files if f.endswith('.jinja')]:
                with open(os.path.join(path, jinja_file), "r") as jinja_in:
                    with open(os.path.join(path, jinja_file).replace('.jinja', ''), "w") as jinja_out:
                        jinja_out.write(Template(jinja_in.read()).render(self.context))
                os.unlink(os.path.join(path, jinja_file))

    def _find_choices(self):
        for path, dirs, files in os.walk(self.temp_dir):
            if 'forger.json' in files:
                return path, os.path.join(path, 'forger.json')
        return self.temp_dir, None


class ZipClonedCast(ClonedCast):
    def do_clone(self):
        r = requests.get(self.location)
        data = StringIO(r.content)
        with zipfile.ZipFile(data, "r") as archive:
            archive.extractall(self.temp_dir)


class GitClonedCast(ClonedCast):
    def do_clone(self):
        os.system("git clone %s %s" % (self.location, self.temp_dir))


class HgClonedCast(ClonedCast):
    def do_clone(self):
        os.system("hg clone %s %s" % (self.location, self.temp_dir))
