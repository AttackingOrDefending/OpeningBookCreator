from buildutils import get_next_lichess_db_name
from buildutils import get_lichess_db_url
from buildutils import zip_path, source_path
from utils import store_url
import os.path
import requests
import chess.variant


def get_lichess_db(variant, env):
    dbname = get_next_lichess_db_name(zip_path(env), variant)
    dburl = get_lichess_db_url(variant, dbname)
    dbpath = os.path.join(zip_path(env), dbname)
    print("retrieving {}".format(dbname))
    store_url(dburl, dbpath)


def lines_to_pgn(lines, store_file):
    with open(store_file, "a") as file:
        for line in lines.split("\n"):
            text = '[Event ""]\n\n'
            board = chess.variant.AntichessBoard()
            moves = line.split()
            if not moves:
                continue
            for move in moves:
                board.push(board.parse_uci(move))
            text += chess.variant.AntichessBoard().variation_san(board.move_stack)
            text += "\n\n"
            file.write(text)


def download_watkins(env, n=1000):
    if n == 1000:
        filenames = ['easy12.lines', 'e3c6.lines', 'e3Nc6.lines', 'e3Nh6.lines', 'e3g5.lines', 'e3b5.lines', 'e3e6.lines', 'e3c5.lines', 'e3b6.lines']
    elif n == 10000:
        filenames = ['easy12lines.10K', 'e3c6lines.10K', 'e3Nc6lines.10K', 'e3Nh6lines.10K', 'e3g5lines.10K', 'e3b5lines.10K', 'e3e6lines.10K', 'e3c5lines.10K', 'e3b6lines.10K']
    else:
        filenames = ['easy12lines.25K', 'e3c6lines.25K', 'e3Nc6lines.25K', 'e3Nh6lines.25K', 'e3g5lines.25K', 'e3b5lines.25K', 'e3e6lines.25K', 'e3c5lines.25K', 'e3b6lines.25K']
    lines = ""
    for file in filenames:
        url = f"https://magma.maths.usyd.edu.au/~watkins/LOSING_CHESS/{file}"
        text = requests.get(url).text
        lines += text
        lines += "\n\n"
    lines_to_pgn(lines, os.path.join(source_path(env), "lines.pgn"))


download_watkins("antichess", 25000)
