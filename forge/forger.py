#!/usr/bin/env python
from __future__ import print_function
import argparse
from sources import SourceRegistry


class Forger(object):
    def __init__(self):
        self.sources = SourceRegistry()
        self.sources.add('tests/casts.json')
        self.sources.add('http://localhost:5000')
        self.sources.add('http://casts.nimbostratus.de')

    def run(self, args):
        getattr(self, "do_" + args.subcommand)(args)

    def do_search(self, args):
        results = self.sources.search(args.expression)
        key_width = max([len(k) for k in results.keys()]) + 1
        format_str = "%-" + str(key_width) + "s %s"
        for k, v in results.items():
            print(format_str % (k, v['description']))

    def do_clone(self, args):
        cast = self.sources.get_cast(args.name)
        cast.clone(args.directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="forge a project")
    subparsers = parser.add_subparsers(help="command mode", dest="subcommand")

    search = subparsers.add_parser('search', help="search casts")
    search.add_argument('expression', help="search expression")

    build = subparsers.add_parser('clone', help='clone a cast')
    build.add_argument('name', help="the cast to clone")
    build.add_argument('--directory', help="destination directory", default=".")

    Forger().run(parser.parse_args())
