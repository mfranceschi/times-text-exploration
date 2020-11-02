
import os
import random
import re
from typing import List


DATASETS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/datasets/"


def make_list_of_files(nbr: int = -1, random_pick: bool = False) -> List[str]:
    """
    Returns the list of the "la******" files from the folder DATASETS_FOLDER.

    :param nbr: limits the length of the result list; negative value means all files.
    :param random_pick: if true then the files returned are randomly picked, else it is in the alphabetical order of the files.
    :return: A list of filepaths as strings.
    """
    PATTERN = re.compile(r"la[0-9]{6}")
    la_files_in_dir = [
        f"{DATASETS_FOLDER}{filename}" for filename in os.listdir(DATASETS_FOLDER)
        if os.path.isfile(os.path.join(DATASETS_FOLDER, filename)) and PATTERN.match(filename)
    ]
    if nbr < 0:
        nbr = len(la_files_in_dir)

    if random_pick:
        return random.sample(population=la_files_in_dir, k=nbr)
    else:
        return [current_la_file for current_la_file in la_files_in_dir[:nbr]]
