import argparse

from psutil import Process

import utilities
from global_values import *
from inverted_file import InvertedFile
from main import run_search


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--request", "-r",
        help="User request, use quotes to handle multiwords request (with whitespaces between keywords)",
        type=str)
    parser.add_argument("--voc", help="Filename of the VOC", type=str, default=DEFAULT_VOC_FILE)
    parser.add_argument("--pl", help="Filename of the PL", type=str, default=DEFAULT_PL_FILE)
    parser.add_argument("--reg", help="Filename of the Doc Register", type=str, default=DEFAULT_REGISTER_FILE)
    parser.add_argument("--time", "-t", help="Output runtime in milliseconds", action="store_true")
    parser.add_argument(
        "--memory", "-m",
        help="Last output line is the RAM used in bytes (diff between start and end RAM values)",
        action="store_true")
    args = parser.parse_args()

    pr = Process()
    start_time = utilities.timepoint()
    start_ram = pr.memory_info().rss

    inverted_file = InvertedFile.read_from_files(args.voc, args.pl, args.reg)

    user_keywords = utilities.convert_str_to_tokens(args.request)
    run_search(user_keywords, inverted_file)

    end_time = utilities.timepoint()
    end_ram = pr.memory_info().rss
    if args.time:
        print(int(1000 * (end_time - start_time)))
    if args.memory:
        print(end_ram - start_ram)


if __name__ == "__main__":
    main()
