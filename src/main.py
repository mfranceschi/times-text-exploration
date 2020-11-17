from typing import *

from doc_parser import parse_document
from document import Document
from inverted_file import InvertedFile
from pl import PL, PL_PythonLists
from utilities import make_list_of_files, timepoint, convert_str_to_tokens
from voc import VOC, VOC_Hashmap


def run_search(user_keywords: List[str], inverted_file: InvertedFile) -> None:
    results: List[Document] = inverted_file.request_words_disjonctive(user_keywords)

    if results:
        print(f"Found {len(results)} results:")
        for req_res in results:
            print(f"> {req_res.doc} with score={req_res.score}")
    else:
        print("No results found.")


def build_if(voc: VOC, pl: PL, nbr_files: int, random_files: bool, to_read_only: bool) -> InvertedFile:
    inverted_file = InvertedFile(voc=voc, pl=pl)
    list_of_files = make_list_of_files(nbr=nbr_files, random_pick=random_files)
    for file in list_of_files:
        parse_document(file, inverted_file)
    inverted_file.compute_scores()
    if to_read_only:
        inverted_file.convert_to_read_only()
    return inverted_file


if __name__ == "__main__":
    user_input = "violence vIOLeNce,,, VIOLENCE"  # or input()
    user_keywords = convert_str_to_tokens(user_input)  # (word for word in user_input.split())
    start = timepoint()

    inverted_file = build_if(VOC_Hashmap(), PL_PythonLists(), nbr_files=4, random_files=True, to_read_only=True)
    index = 0
    for item in inverted_file.voc.iterate2():
        print(item)
        index += 1
        if index > 25:
            break

    # run_search(user_keywords=user_keywords, inverted_file=inverted_file)
    end = timepoint()
    print(f"Execution time: {end - start}")
