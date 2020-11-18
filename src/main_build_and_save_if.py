import argparse

from global_values import *
from main import build_if
from pl import PL_PythonLists
import utilities
from voc import VOC_Hashmap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nbfiles", "-n", help="Number of files to read", default=5, type=int)
    parser.add_argument("--shufflefiles", "-s", help="Shuffle the files ordering", action="store_true")
    parser.add_argument("--voc", help="Filename of the VOC", type=str, default=DEFAULT_VOC_FILE)
    parser.add_argument("--pl", help="Filename of the PL", type=str, default=DEFAULT_PL_FILE)
    parser.add_argument("--reg", help="Filename of the Doc Register", type=str, default=DEFAULT_REGISTER_FILE)
    parser.add_argument("--do_not_save", help="Generate in-memory but do not save in files", action="store_true")
    parser.add_argument("--time", "-t", help="Output runtime in milliseconds", action="store_true")
    args = parser.parse_args()

    start_time = utilities.timepoint()
    inverted_file = build_if(
        voc=VOC_Hashmap(),
        pl=PL_PythonLists(),
        nbr_files=args.nbfiles,
        random_files=args.shufflefiles)

    if not args.do_not_save:
        inverted_file.write_to_files(
            args.voc,
            args.pl,
            args.reg)

    end_time = utilities.timepoint()
    if args.time:
        print(int(1000 * (end_time - start_time)))


if __name__ == "__main__":
    main()
