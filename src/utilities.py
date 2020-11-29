import pickle
import random
import re
import time
from pathlib import Path
from typing import Any, List, Set

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


def create_empty_file_with_size(file: str, size: int, erase_if_present: bool) -> None:
    """
    Creates a file and make it have the given size.
    If it already exists and "erase_if_present", the original is erased.
    If it already exists and not "erase_if_present", the original's size is unchanged OR increased.
    """
    p = Path(file)
    if p.exists() and erase_if_present:
        p.unlink()
        p.touch()

    with open(file=file, mode="wb+", buffering=0) as opened_file:
        opened_file.seek(size - 1)
        opened_file.write(b"0")


def timepoint() -> float:
    """
    Gets the current time in seconds.
    """
    return time.perf_counter()


def convert_str_to_tokens(data: str) -> List[str]:

    # Portier's method: I don't think we will use it, it requires us more work.
    # import nltk
    # tokenizer = nltk.tokenize.casual_tokenize(data)

    from doc_parser import pre_work_word
    tokenizer = list(set([pre_work_word(word)
                          for word in data.split() if pre_work_word(word)]))
    # Pre-work each word then ensure unique. Unfortunately it sorts words.

    return tokenizer


def get_stop_words() -> Set[str]:
    with open(Path(__file__).parent.parent / "english_stopwords.txt") as f:
        # In Python a set is a hash-set --> lookup is log(1).
        lines = f.readlines()
    return set((word.strip() for word in lines))


def write_pyobj_to_disk(obj, filename: str):
    with open(filename, "wb+") as f:
        pickle.dump(obj, f)


def read_pyobj_from_disk(filename: str) -> Any:
    with open(filename, "rb") as f:
        return pickle.load(f)


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
