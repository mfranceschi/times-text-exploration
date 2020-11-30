import argparse

from psutil import Process

import gc
import utilities
from global_values import *
from inverted_file import InvertedFile
from main import run_search
import voc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--request", "-r",
        help="User request, use quotes to handle multiwords request (with whitespaces between keywords)",
        type=str)
    parser.add_argument("--voc", help="Filename of the VOC", type=str, default=DEFAULT_VOC_FILE)
    parser.add_argument("--pl", help="Filename of the PL", type=str, default=DEFAULT_PL_FILE)
    parser.add_argument("--reg", help="Filename of the Doc Register", type=str, default=DEFAULT_REGISTER_FILE)
    parser.add_argument("--voc_type", help="Type of the PL to instantiate", type=str, default="VOC_Hashmap")
    parser.add_argument("--time", "-t", help="Output runtime in milliseconds", action="store_true")
    parser.add_argument(
        "--memory", "-m",
        help="Last output line is the RAM used in bytes (diff between start and end RAM values)",
        action="store_true")
    args = parser.parse_args()

    pr = Process()
    start_time = utilities.timepoint()
    start_ram = pr.memory_info().rss

    voc_type: type = eval(f"voc.{args.voc_type}")
    inverted_file = InvertedFile.read_from_files(args.voc, args.pl, args.reg, voc_type)

    user_keywords = utilities.convert_str_to_tokens(args.request)
    run_search(user_keywords, inverted_file)

    end_time = utilities.timepoint()
    gc.collect()
    end_ram = pr.memory_info().rss
    output_str = ""
    if args.time:
        output_str += f"Runtime(ms) {int(1000 * (end_time - start_time))}"
    if args.time and args.memory:
        output_str += " "
    if args.memory:
        output_str += f"Memory(bytes) {end_ram - start_ram}"
    print(output_str)


if __name__ == "__main__":
    main()
