from __future__ import absolute_import

from typing import *
import time

from document import Document
from inverted_file import InvertedFile
from pl import PL_PythonLists
from utilities import make_list_of_files
from doc_parser import parse_document
from voc import VOC_Hashmap


def run_search(user_keywords: List[str], inverted_file: InvertedFile) -> None:
    results: List[Document] = inverted_file.request_words_disjonctive(user_keywords)

    if results:
        print(f"Found {len(results)} results:")
        for req_res in results:
            print(f"> {req_res.doc} with score={req_res.score}")
    else:
        print("No results found.")


if __name__ == "__main__":
    start = time.time()
    user_keywords = ["violence"]  # [word for word in input().split(sep=" ")]
    inverted_file = InvertedFile(voc=VOC_Hashmap(), pl=PL_PythonLists())
    list_of_files = make_list_of_files(nbr=2, random_pick=False)
    for file in list_of_files:
        parse_document(file, inverted_file)
    inverted_file.compute_scores()

    run_search(user_keywords=user_keywords, inverted_file=inverted_file)
    end = time.time()
    print(f"Execution time: {end - start}")
