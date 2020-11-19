import argparse

from psutil import Process

from global_values import *
from main import build_if
from pl import PL_PythonLists
import utilities


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nbfiles", "-n", help="Number of files to read", default=5, type=int)
    parser.add_argument("--shufflefiles", "-s", help="Shuffle the files ordering", action="store_true")

    parser.add_argument("--voc", help="Filename of the VOC", type=str, default=DEFAULT_VOC_FILE)
    parser.add_argument("--pl", help="Filename of the PL", type=str, default=DEFAULT_PL_FILE)
    parser.add_argument("--reg", help="Filename of the Doc Register", type=str, default=DEFAULT_REGISTER_FILE)

    parser.add_argument("--voc_type", help="Class name of the VOC to instantiate", type=str, default="VOC_Hashmap")
    # parser.add_argument("--pl_type", help="Class name of the PL to instantiate", type=str, default="PL_PythonLists")

    parser.add_argument("--do_not_save", help="Generate in-memory but do not save in files", action="store_true")
    parser.add_argument("--time", "-t", help="Output runtime in milliseconds", action="store_true")
    parser.add_argument(
        "--memory", "-m",
        help="Last output line is the RAM used in bytes (diff between start and end RAM values)",
        action="store_true")
    args = parser.parse_args()

    pr = Process()
    start_time = utilities.timepoint()
    start_ram = pr.memory_info().rss
    inverted_file = build_if(
        voc=eval(f"voc.{args.voc_type}()"),
        pl=PL_PythonLists(),
        nbr_files=args.nbfiles,
        random_files=args.shufflefiles)

    if not args.do_not_save:
        inverted_file.write_to_files(
            args.voc,
            args.pl,
            args.reg)

    end_time = utilities.timepoint()
    end_ram = pr.memory_info().rss
    if args.time and False:
        print(int(1000 * (end_time - start_time)))

    print(f"Runtime(ms) {int(1000 * (end_time - start_time))} Memory(bytes) {end_ram - start_ram}")
    if args.memory and False:
        print(end_ram - start_ram)


if __name__ == "__main__":
    main()
