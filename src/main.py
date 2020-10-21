from __future__ import absolute_import

from typing import *

from document import Document
from inverted_file import InvertedFile
from utilities import make_list_of_files
from doc_parser import parse_document


user_keywords = ["Antony"]  # [word for word in input().split(sep=" ")]

inverted_file = InvertedFile()
list_of_files = make_list_of_files(2)
for file in list_of_files:
    parse_document(file, inverted_file)

results: List[Document] = inverted_file.request_words_conjonctive(user_keywords) # [Document(id=2, title="Photos géniales, la 7e va vous surprendre")]

if results:
    print(f"Found {len(results)}:")
    for document in results:
        print(f"> {document} with score={1}")
else:
    print("No results found.")
