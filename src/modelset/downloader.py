import os
import shutil
import sys
import tempfile
from argparse import ArgumentParser

import wget

URL_ZIP_MODELSET = 'https://github.com/modelset/modelset-dataset/releases/download/v0.9.3/modelset.zip'
DEFAULT_DIR_MODELSET = os.path.join(os.path.expanduser('~'), '.modelset', 'modelset')
URL_WORD2VEC = 'http://sanchezcuadrado.es/files/modelset/vectors.kv'
WORD2VEC_NAME_KV = 'vectors.kv'


def download_modelset(args):
    tempdir = tempfile.gettempdir()
    filename = wget.download(URL_ZIP_MODELSET, out=tempdir)
    shutil.unpack_archive(filename, extract_dir=tempdir)
    shutil.move(os.path.join(tempdir, "modelset"), args.output_dir)
    os.remove(filename)


def download_word2vec(args):
    wget.download(URL_WORD2VEC, out=args.output_dir)


def main(args):
    try:
        download_modelset(args)
    except:
        print('Cannot download ModelSet', file=sys.stderr)
    try:
        download_word2vec(args)
    except:
        print('Cannot download Word2vec4MDE', file=sys.stderr)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output_dir",
                        help="Directory where modelset is going to be placed",
                        default=DEFAULT_DIR_MODELSET)
    args = parser.parse_args()
    main(args)
