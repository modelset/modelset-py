import os
import shutil
from argparse import ArgumentParser

import wget

URL_ZIP_MODELSET = 'https://github.com/modelset/modelset-dataset/releases/download/v0.9.3/modelset.zip'
DEFAULT_DIR_MODELSET = os.path.join(os.path.expanduser('~'), '.modelset')


def main(args):
    filename = wget.download(URL_ZIP_MODELSET, out=args.output_dir)
    shutil.unpack_archive(filename, extract_dir=args.output_dir)
    os.remove(filename)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output_dir",
                        help="Directory where modelset is going to be placed",
                        default=os.path.expanduser('~'))
    args = parser.parse_args()
    main(args)
