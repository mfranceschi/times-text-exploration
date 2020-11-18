# Testing the **psutil** module for benchmarks and measurements.
# Reference: https://psutil.readthedocs.io/en/latest/

from typing import Tuple
import psutil

from main import build_if
from pl import PL_PythonLists
from voc import VOC_Hashmap
from utilities import timepoint


def fmt(num: int, suffix: str = 'B') -> str:
    """
    From https://stackoverflow.com/a/1094933
    Converts an amount of bytes to a human-readable version.
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_ram(p: psutil.Process) -> int:
    return p.memory_info().rss


def get_cpu_times(p: psutil.Process) -> Tuple[int, int]:
    named_tuple = p.cpu_times()
    return named_tuple.user, named_tuple.system


if __name__ == "__main__":
    p = psutil.Process()  # Get an instance using the current PID

    initial_ram = get_ram(p)
    initial_user_time, initial_kernel_time = get_cpu_times(p)
    initial_time = timepoint()
    print(
        "Before run",
        f"RAM={fmt(initial_ram)}, CPU User time={initial_user_time}, CPU Kernel time={initial_kernel_time}",
        "",
        sep="\n"
    )

    inverted_file = build_if(VOC_Hashmap(), PL_PythonLists(), nbr_files=100, random_files=False, to_read_only=False)

    new_ram = get_ram(p)
    new_user_time, new_kernel_time = get_cpu_times(p)
    final_time = timepoint()

    print(
        "",
        "After run",
        f"RAM={fmt(new_ram)}, CPU User time={new_user_time}, CPU Kernel time={new_kernel_time}",
        f"\nRun duration={final_time - initial_time}"
        "",
        sep="\n"
    )

"""
Pistes possibles :
- p.num_ctx_switches()
- p.io_counters() (pas sous Apple)
"""
