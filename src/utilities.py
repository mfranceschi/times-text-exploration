from pathlib import Path
import random
import re
from typing import List


DATASETS_FOLDER = Path(__file__).parent.parent / "datasets"
PATTERN = re.compile(r"la[0-9]{6}.xml")


def make_list_of_files(nbr: int = -1, random_pick: bool = False) -> List[str]:
    """
    Returns the list of the "la******" files from the folder DATASETS_FOLDER.

    :param nbr: limits the length of the result list; negative value means all files.
    :param random_pick: files are randomly picked, or in alphabetical order.
    :return: A list of filepaths as strings.
    """
    la_files_in_dir: List[Path] = []
    for filename in DATASETS_FOLDER.iterdir():
        if filename.is_file() and PATTERN.match(filename.name):
            la_files_in_dir.append(filename)

    if nbr < 0:
        nbr = len(la_files_in_dir)

    if random_pick:
        return random.sample(population=la_files_in_dir, k=nbr)
    else:
        return [str(current_la_file) for current_la_file in la_files_in_dir[:nbr]]


def create_empty_file_with_size(file: str, size: int) -> None:
    """
    Creates a file and make it have the given size.
    If it already exists, the original is erased.
    """
    if Path(file).exists():
        Path(file).unlink()

    with open(file=file, mode="wb+", buffering=0) as opened_file:
        opened_file.seek(size - 1)
        opened_file.write(b"\0")
