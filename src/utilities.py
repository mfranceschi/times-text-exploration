
import os
import re
from typing import *

DATASETS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/datasets/"


def make_list_of_files(nbr: int=-1) -> List[str]:
    """
    Returns the list of the "la******" files from the folder DATASETS_FOLDER.
    "nbr" limits the length of the result list; negative value means all files.
    """
    PATTERN = re.compile(r"la[0-9]{6}")
    la_files_in_dir = [filename for filename in os.listdir(DATASETS_FOLDER) if os.path.isfile(os.path.join(DATASETS_FOLDER, filename)) and PATTERN.match(filename)]
    if nbr < 0:
        nbr = len(la_files_in_dir)
    to_return = [DATASETS_FOLDER + la_file for la_file in la_files_in_dir[:nbr]]
    return to_return
