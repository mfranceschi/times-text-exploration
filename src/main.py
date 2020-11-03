from __future__ import absolute_import

from typing import *

from document import Document
from inverted_file import InvertedFile
from utilities import make_list_of_files
from doc_parser import parse_document


def run_search(user_keywords: List[str], inverted_file: InvertedFile) -> None:
    results: List[Document] = inverted_file.request_words_conjonctive(user_keywords)
    # [Document(id=2, title="Photos géniales, la 7e va vous surprendre")]

    if results:
        print(f"Found {len(results)} results:")
        for req_res in results:
            print(f"> {req_res.doc} with score={req_res.score}")
    else:
        print("No results found.")


if __name__ == "__main__":
    user_keywords = ["book"]  # [word for word in input().split(sep=" ")]
    inverted_file = InvertedFile()
    list_of_files = make_list_of_files(nbr=2, random_pick=True)
    for file in list_of_files:
        parse_document(file, inverted_file)

    run_search(user_keywords=user_keywords, inverted_file=inverted_file)
