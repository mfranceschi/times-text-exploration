import string
from os import path
from typing import List

from document import Document
from inverted_file import InvertedFile
from xml.dom import minidom


with open(path.join(path.dirname(path.dirname(path.abspath(__file__))), "english_stopwords.txt")) as f:
    STOP_WORDS = f.readlines()
ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits


def pre_work_word(word: str) -> str:
    """
    Context-independent preprocessing of word.
    TODO later: remove stop words, remove punctuation, tokenize, stem...
    Returns the corrected string, or the empty string if we decide to ignore that word.
    """

    # Skip if the argument is not interesting.
    if not word:
        return ""

    # Convert to lowercase
    word = word.lower()

    # Remove non-letters characters at the beginning and at the end
    while word and word[0] not in ALLOWED_CHARACTERS:
        word = word[1:]
    while word and word[-1] not in ALLOWED_CHARACTERS:
        word = word[:-1]

    # Remove stop words
    if word in STOP_WORDS:
        word = ""

    return word


def parse_document(filename: str, invf: InvertedFile):
    # https://docs.python.org/fr/3/library/xml.dom.html#module-xml.dom
    print(f"Filename : {filename}")
    with open(filename, "r") as f:
        document_text = f.read()

    document_text_without_line_breaks = document_text.replace("\n", "")
    fixed_document = f"<customroot>{document_text_without_line_breaks}</customroot>"
    dom_document = minidom.parseString(fixed_document)
    root_element = dom_document.documentElement

    for document_node in root_element.childNodes:
        document_instance = Document()
        document_instance.id = int(document_node.getElementsByTagName("DOCID")[0].firstChild.data.strip())
        document_instance.no = document_node.getElementsByTagName("DOCNO")[0].firstChild.data.strip()
        # print(f"We study docid {document_instance.id}")

        # Get the Title and Subtitle of the article
        list_of_headline_elements = document_node.getElementsByTagName("HEADLINE")
        if not list_of_headline_elements:
            # We skip the article if there is no headline element.
            continue
        headline_texts = ""
        for paragraph_element in list_of_headline_elements[0].childNodes:
            if paragraph_element.firstChild and paragraph_element.tagName == "P":
                headline_texts += paragraph_element.firstChild.data
        # print(headline_texts)
        document_instance.title = headline_texts

        # Get article's main paragraphs
        list_of_text_elements = document_node.getElementsByTagName("TEXT")
        if not list_of_text_elements:
            # TODO maybe not skip
            continue
        text_element = list_of_text_elements[0]
        text_paragraphs = ""
        for paragraph_element in text_element.childNodes:
            if paragraph_element.firstChild and paragraph_element.tagName == "P":
                text_paragraphs += paragraph_element.firstChild.data
        # document_instance.text = text_paragraphs

        # Send the document to the IF
        invf.register_document(document_instance)

        # For each word in the doc, send it to the IF
        words: List[str] = []
        for word in text_paragraphs.split():
            word_to_add = pre_work_word(word)
            if word_to_add:
                words.append(word_to_add)

        freq = {word: words.count(word) for word in words}
        for word, nbr in freq.items():
            invf.notify_word_appeared(word, document_instance.id, nbr)
