import os
import yaml
import shutil
import requests
import pathlib
import zstandard


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("created directory {}".format(path))
    else:
        # print("{} exists".format(path))
        pass


def write_string_to_file(path, str, force=True):
    if os.path.isfile(path) and not force:
        return
    with open(path, "w") as outfile:
        outfile.write(str)
    print("written file {} ( {} characters )".format(path, len(str)))


def read_string_from_file(path, default):
    try:
        content = open(path).read()
        return content
    except Exception:
        return default


def load_yaml(path):
    try:
        with open(path, 'r') as stream:
            obj = yaml.safe_load(stream)
            return obj
    except Exception:
        return {}


def dump_yaml(path, obj):
    write_string_to_file(path, yaml.dump(obj))


def store_url(url, path):
    total_bytes = 0
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(path, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    out_file.write(chunk)
                    total_bytes += 1024
        print("retrieved {} to {} ( {} bytes )".format(url, path, total_bytes))


def get_ext(path):
    parts = path.split(".")
    return parts[-1]


def unzip(frompath, topath, force):
    if os.path.isfile(topath) and not force:
        return
    print("unzipping {} to {}".format(frompath, topath))
    if get_ext(frompath) == "zst":
        input_file = pathlib.Path(frompath)
        with open(input_file, 'rb') as compressed:
            decomp = zstandard.ZstdDecompressor()
            output_path = pathlib.Path(topath) / input_file.stem
            with open(output_path, 'wb') as destination:
                decomp.copy_stream(compressed, destination)
    else:
        shutil.unpack_archive(frompath, topath)
