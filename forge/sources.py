import json
import requests
import logging
from casts import Cast

try:
    from urlparse import urlparse
except ImportError:
    from urllib import parse as urlparse


class Source(object):
    def __init__(self, location):
        self.location = urlparse(location)

    def search(self, expression):
        return {}

    def get(self, name):
        return {}


class FilesystemSource(Source):
    def search(self, expression):
        with open(self.location.path, "r") as infile:
            candidates = json.loads(infile.read())
            return {
                k: v
                for k, v in candidates.items()
                if expression.lower() in k.lower()
                or expression.lower() in v['description'].lower()
            }

    def get(self, name):
        with open(self.location.path, "r") as infile:
            try:
                return json.loads(infile.read())[name]
            except KeyError:
                return {}


class HttpSource(Source):
    def search(self, expression):
        try:
            request = requests.get(
                self.location.geturl() + '/search',
                params={"expression": expression})
        except requests.exceptions.ConnectionError:
            logging.warning('could not retrieve source %(source)s (not reachable).' % {
                'source': self.location.geturl(),
            })
            return {}
        try:
            return request.json()
        except ValueError:
            logging.warning('could not retrieve source %(source)s (%(status)s).' % {
                'source': self.location.geturl(),
                'status': request.status_code
            })
        return {}

    def get(self, name):
        request = requests.get(
            self.location.geturl() + '/get',
            params={"name": name})
        try:
            return request.json()
        except ValueError:
            return {}


class SourceRegistry(object):

    def __init__(self, sources=None):
        self.sources = sources or []

    def add(self, location):
        if urlparse(location).scheme in ["file", ""]:
            self.sources.append(FilesystemSource(location))
        else:
            self.sources.append(HttpSource(location))

    def search(self, expression):
        results = {}
        for source in self.sources:
            results.update(source.search(expression))
        return results

    def get_cast(self, name):
        result = {}
        for source in self.sources:
            result.update(source.get(name))
        return Cast(**result)

