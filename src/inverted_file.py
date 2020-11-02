
from typing import List

import BTrees

from document import Document

# https://pythonhosted.org/BTrees/
# https://btrees.readthedocs.io/en/latest/


class RequestResult:
    def __init__(self, doc: Document, score: int) -> None:
        self.doc = doc
        self.score = score


# https://www.geeksforgeeks.org/python-positional-index/
# https://pypi.org/project/diskhash/
class InvertedFile:
    class VOCPair:
        def __init__(self, term: str = "", size_pl: int = 0) -> None:
            self.term = term
            self.size_pl = size_pl
            pass

    def __init__(self) -> None:
        self.documents_catalog: List[Document] = []
        self.voc = ""  # allez y faites votre b tree
        self.pl = ""  # todo la veille du rendu
        pass

    def register_document(self, doc: Document) -> None:
        self.documents_catalog.append(doc)

    def notify_word_appeared(self, word: str, docID: int, occurences: int = 1) -> None:
        """
        When parsing a document, this function takes note that the given word appeared in the given file.
        This may be called several times with the same word, we increment the number of occurences.
        """
        pass

    def request_words_conjonctive(self, words: List[str]) -> List[RequestResult]:
        return []


# VOC  = {paire<"terme",taille PL>, offset PL }
# PL = objet continu en disque, accédé en mode "octet par octet".
# Idées en vrac:
# -> La PL est un tableau continu en mémoire, tableau de paires<docID,score> pour chaque terme. 
#   - Ainsi, taille et offset nous indiquent où aller et combien d'octets lire (par exemple, les 4 premiers octets sont le docID, etc.°.
#   - Problème : mettons que j'ai "dog" dans le doc 1, puis "cat" dans le doc 2. J'écris l'entrée pour "cat" au premier emplacement dispo, donc après "dog". Maintenant, j'ai encore "dog" dans le doc 3 : il faut que je décalle l'entrée pour "cat" ? Et même problème par exemple si un mot comme "London" apparait un doc sur deux, très compliqué.
# -> Pareil, mais les paires consécutives ne sont pas associées au même terme, et la VOC indiquerait alors une liste d'offsets.
#   - On peut paralléliser les accès à la PL pour chaque terme, genre 1 thread par offset.
#   - Problème : la mémoire consommée pour stocker la liste d'offsets casse l'intérêt. Si la paire de la PL fait 8 octets et mon offset fait 8 octets (typique en 64 bits), c'est con quoi.
# -> La PL est un tableau continu en mémoire, tableau de tuples<docID, score, next> pour chaque terme, avec "next" l'offset du prochain terme.
#   - Logique d'une liste chaînée qui résout les problèmes des ArrayList par exemple. Limite on n'a pas besoin de la taille de la PL. 
#   - Problème : peut-être pas compatible avec les attentes de PEP ?

# (pas à jour)
# Exemple : je cherche "dog"
# TODO
# J'ai donc une liste de paires<docID, scores>
# Gagné
