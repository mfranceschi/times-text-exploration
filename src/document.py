
from xml.dom import minidom

class Document:
    def __init__(self, id: int=0, title: str="", no: str="", text: str=""):
        self.id = id
        self.title = title
        self.no = no
        self.text = text
    
    def __str__(self) -> str:
        return f"Document[id={self.id},title={self.title}]"

def pre_work_word(word: str) -> str:
    """
    Context-independent preprocessing of word.
    TODO later: remove stop words, tokenize, stem...
    """
    return word

def parse_document(filename: str):
    # https://docs.python.org/fr/3/library/xml.dom.html#module-xml.dom
    print(f"Filename : {filename}")
    with open(filename, "r") as f:
        document_text = f.read()

    document_text_without_line_breaks = document_text.replace("\n","")
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
        document_instance.text = text_paragraphs
        
    """
    text = "bonjouuuur"
    # TODO open file, parse XML, fetch infos, make Document instance
    lines = text.splitlines(keepends=False)
    words = []
    for line in lines:
        words_in_line = line.split(sep=" ")
        for word in words_in_line:
            word_to_add = pre_work_word(word)
            if word_to_add:
                words.append(word_to_add)
    """
    # TODO notify the IF for each word in words
