import argparse
from utils import read_string_from_file
from utils import unzip
from downloads import get_lichess_db, download_watkins
from buildutils import create_env
from buildutils import load_defaults
from buildutils import dump_defaults
from buildutils import env_path
from buildutils import zip_path
from buildutils import source_path
from buildutils import filtered_path
from buildutils import book_path
from buildutils import BasePgnVisitor
from buildutils import visit_pgn_file
from book import build_book_file
from book import Book
import os


class FilterVisitor(BasePgnVisitor):
    def __init__(self, outfile, filter_logic):
        super(FilterVisitor, self).__init__()
        self.filter_logic = filter_logic
        self.outfile = outfile
        self.found = 0

    def show_info(self):
        print("found {} games".format(self.found))

    def process(self):
        self.ok = True

        exec(self.filter_logic)

        if self.ok:
            self.found += 1
            self.outfile.write(self.pgn + "\n\n\n")


#########################################################################
# setup args and defaults

parser = argparse.ArgumentParser(description='Filter PGN files and build a book from them')

parser.add_argument('-e', '--env', help='create / activate build environment')
parser.add_argument('-u', '--unzip', action="store_true", help='unzip files in zip folder to pgn folder')
parser.add_argument('-f', '--filter', action="store_true", help='filter files in source folder to filtered folder')
parser.add_argument('-b', '--build', action="store_true", help='build polyglot book')
parser.add_argument('-a', '--all', action="store_true", help='unzip, filter, build')
parser.add_argument('-m', '--merge', action="store_true", help='merge books')
parser.add_argument('--force', action="append", help='force [ env , unzip , filter , build ]')
parser.add_argument('--variant', action="store", help='variant')
parser.add_argument('--nextlichessdb', action="store_true", help='download next lichess db')
parser.add_argument('--watkins', action="store_true", help='download the proof lines from the antichess solution')

args = parser.parse_args()


def get_force(key):
    if not args.force:
        return False
    return key in args.force


defaults = load_defaults()

if "env" not in defaults:
    defaults["env"] = None

env = defaults["env"]


def assert_env():
    if env is None:
        raise Exception("EnvironmentMissing")


if args.variant is not None:
    defaults["variant"] = args.variant

if "variant" not in defaults:
    defaults["variant"] = "standard"

variant = defaults["variant"]

print("------")

#########################################################################
# command interpreter

if args.env is not None:
    env = args.env
    print("creating / activating environment {}".format(env))
    create_env(env, get_force("env"))
    print("environment {} created ok".format(env))
    defaults["env"] = env

if args.nextlichessdb:
    assert_env()
    get_lichess_db(variant, env)

if args.watkins:
    assert_env()
    download_watkins(env, args.watkins)

if args.unzip or args.all:
    assert_env()
    for name in os.listdir(zip_path(env)):
        zippath = os.path.join(zip_path(env), name)
        sourcepath = source_path(env)
        unzip(zippath, sourcepath, get_force("unzip"))

if args.filter or args.all:
    assert_env()
    filter_logic_path = os.path.join(env_path(env), "filter_logic.py")
    filter_logic = read_string_from_file(filter_logic_path, "")
    for name in os.listdir(source_path(env)):
        pgnpath = os.path.join(source_path(env), name)
        filteredpath = os.path.join(filtered_path(env), name)
        if (not os.path.isfile(filteredpath)) or get_force("filter"):
            visitor = FilterVisitor(open(filteredpath, "w"), filter_logic)
            visit_pgn_file(pgnpath, visitor)
            pass

if args.build or args.all:
    assert_env()
    for name in os.listdir(filtered_path(env)):
        filteredpath = os.path.join(filtered_path(env), name)
        bookpath = os.path.join(book_path(env), name) + ".bin"
        if (not os.path.isfile(bookpath)) or get_force("build"):
            build_book_file(filteredpath, bookpath)

if args.merge or args.all:
    assert_env()
    book = Book()
    for name in os.listdir(book_path(env)):
        bookpath = os.path.join(book_path(env), name)
        mergepath = os.path.join(env_path(env), "merged.bin")
        print("merging {}".format(bookpath))
        book.merge_file(bookpath)
    book.normalize_weights()
    book.save_as_polyglot(mergepath)

#########################################################################
# store defaults

dump_defaults(defaults)

print(defaults)

print("------\nactive environment > {} ( variant {} )".format(defaults["env"], defaults["variant"]))
