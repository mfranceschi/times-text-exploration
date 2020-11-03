from collections import defaultdict
from typing import List, Dict, Tuple

import BTrees
from doc_parser import pre_work_word

from document import Document

# https://pythonhosted.org/BTrees/
# https://btrees.readthedocs.io/en/latest/


class RequestResult:
    def __init__(self, doc: Document, score: int) -> None:
        self.doc = doc
        self.score = score

    def __str__(self) -> str:
        return f"RequestResult[doc={self.doc}, score={self.score}]"


# https://www.geeksforgeeks.org/python-positional-index/
# https://pypi.org/project/diskhash/

class VOCEntry:
    """
    This tuple is the value type of the "voc" dict.
    Beign known the word, it gives the Posting List's size and identifier.
    Identifier = how to retrieve it (interpretation changes depending on the PL data structure).
    """
    def __init__(self, pl_identifier: int, size_pl: int) -> None:
        self.pl_id = pl_identifier
        self.size_pl = size_pl


class PLEntry:
    """
    This tuple, given a known word, associates to it a document and a score.
    """
    def __init__(self, docID: int = 0, score: int = 0) -> None:
        self.docID = docID
        self.score = score


class InvertedFile:
    def __init__(self) -> None:
        self.documents_catalog: List[Document] = []
        self.voc: Dict[str, VOCEntry] = defaultdict()  # Associates a word with infos about the PL.
        self.pl: List[List[PLEntry]] = []  # pl[i] gives the PL of the word which metadata indicates that the PL ID is i.

    def register_document(self, doc: Document) -> None:
        self.documents_catalog.append(doc)

    def get_document_by_id(self, id: int) -> Document:
        for doc in self.documents_catalog:
            if doc.id == id:
                return doc

    def compute_score(self, occurences: int) -> int:
        """
        Given all possible infos, computes and returns a score.
        Current method: count the occurences (TODO: TF-IDF).
        """
        return occurences

    def notify_word_appeared(self, word: str, docID: int, occurences: int) -> None:
        """
        When parsing a document, this function takes note that the given word appeared in the given file.
        This may be called several times with the same word, we increment the number of occurences.
        """
        voc_item = self.voc.get(word)
        new_pl_item = PLEntry(docID=docID, score=self.compute_score(occurences=occurences))

        if voc_item:
            # update pl item and voc item for term
            pl_id = voc_item.pl_id
            pl_list = self.pl[pl_id]

            pl_list.append(new_pl_item)
            voc_item.size_pl += 1
        else:
            # create new instance in voc for term
            new_pl_id = len(self.pl)
            voc_item = VOCEntry(pl_identifier=new_pl_id, size_pl=1)
            self.pl.append([new_pl_item])
            self.voc[word] = voc_item

    def request_words_conjonctive(self, words: List[str]) -> List[RequestResult]:
        request = (pre_work_word(word) for word in words)
        results: List[RequestResult] = []

        for word_to_test in request:
            voc_item = self.voc.get(word_to_test)
            if not voc_item:
                return []

            for pl_entry in self.pl[voc_item.pl_id]:
                doc_id = pl_entry.docID
                document = self.get_document_by_id(doc_id)
                score = pl_entry.score

                # TODO: if the document is already there, don't add a new entry but adapt the score.
                result = RequestResult(doc=document, score=score)
                results.append(result)

        # TODO: as it is a conjonctive request, we must ensure that all documents are in the PLs of all words.

        # Sort by descending order of the scores
        results.sort(key=lambda req_res: req_res.score, reverse=True)
        return results


# memory mapped files
# VOC  = {paire<"terme",taille PL>, offset PL }  hasmap??? (Pidou)
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
