import argparse
from itertools import islice

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
    args = parser.parse_args()

    start_time = utilities.timepoint()
    inverted_file = InvertedFile.read_from_files(args.voc, args.pl, args.reg)
    print(list(islice(((x[1].pl_id, x[1].pl_size) for x in inverted_file.voc.iterate2()), 5)))
    # print([(x[1].pl_id, x[1].pl_size) for x in inverted_file.voc.iterate2()])
    # print([doc.id for doc in inverted_file.register.registry])

    user_keywords = utilities.convert_str_to_tokens(args.request)
    run_search(user_keywords, inverted_file)
    end_time = utilities.timepoint()

    if args.time:
        print(int(1000 * (end_time - start_time)))


if __name__ == "__main__":
    main()
