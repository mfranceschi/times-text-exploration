from __future__ import absolute_import

from typing import *

from document import Document
from inverted_file import InvertedFile
from utilities import make_list_of_files


user_keywords = ["Antony"]  # [word for word in input().split(sep=" ")]

inverted_file = InvertedFile()
inverted_file.parse_docs(make_list_of_files())  # generate the IF (pre-treatments)

results: List[Document] = inverted_file.request_words_conjonctive(user_keywords) # [Document(id=2, title="Photos géniales, la 7e va vous surprendre")]

if results:
    print(f"Found {len(results)}:")
    for document in results:
        print(f"> {document} with score={1}")
else:
    print("No results found.")
