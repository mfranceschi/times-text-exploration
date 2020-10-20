
class Document:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title
    
    def __str__(self) -> str:
        return f"Document[id={self.id},title={self.title}]"

# str(Document(id=2, title="Un titre")) = "Document[id=2,title=Un titre]"

def pre_work_word(word: str) -> str:
    """
    Context-independent preprocessing of word.
    TODO later: remove stop words, tokenize, stem...
    """
    return word

def parse_document(filename: str):
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
    
    # TODO notify the IF for each word in words
