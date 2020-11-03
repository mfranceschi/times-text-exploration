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
