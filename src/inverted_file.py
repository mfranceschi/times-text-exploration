from collections import defaultdict
from math import log
from typing import List, Dict, Tuple

from doc_parser import pre_work_word
from voc import VOC
from pl import PL, PL_InPythonLists, PLEntry

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

class InvertedFile:
    def __init__(self) -> None:
        self.documents_catalog: List[Document] = []
        self.voc: VOC = VOC()
        self.pl: PL = PL_InPythonLists()

    def register_document(self, doc: Document) -> None:
        self.documents_catalog.append(doc)

    def get_document_by_id(self, id: int) -> Document:
        for doc in self.documents_catalog:
            if doc.id == id:
                return doc

    def compute_scores(self):
        """
        When all documents are parsed, we re-compute scores for all PL entries.
        """
        D = len(self.documents_catalog)  # Number total of documents

        for voc_entry in self.voc.voc.values():
            pl_id = voc_entry.pl_id
            pl_size = voc_entry.size_pl

            current_pl = self.pl.get_pl(pl_id=pl_id, size=pl_size)
            for pl_entry in current_pl:
                tf = 1 + log(pl_entry.score)
                idf = log(D / (1 + pl_size))
                final_score = int(100 * tf * idf)
                pl_entry.score = final_score
            self.pl.flush_pl(pl_id=pl_id, new_pl=current_pl)

    def notify_word_appeared(self, word: str, docID: int, occurences: int) -> None:
        """
        When parsing a document, this function takes note that the given word appeared in the given file.
        This may be called several times with the same word, we increment the number of occurences.
        """
        score = occurences
        if self.voc.has_term(word):
            pl_id = self.voc.get_pl_id(word)
            self.pl.update(pl_id, docID, score)
            self.voc.increment_pl_size(word)
        else:
            pl_id = self.pl.create_new_pl(docID, score)
            self.voc.add_entry(word, pl_id)

    def request_words_disjonctive(self, words: List[str]) -> List[RequestResult]:
        request = (pre_work_word(word) for word in words)
        results: List[RequestResult] = []

        for word_to_test in request:
            if self.voc.has_term(word_to_test):
                pl_size = self.voc.get_pl_size(word_to_test)
                pl_id = self.voc.get_pl_id(word_to_test)
                pl_for_that_term: List[PLEntry] = self.pl.get_pl(pl_id=pl_id, size=pl_size)

                for pl_entry in pl_for_that_term:
                    doc_id = pl_entry.docID
                    document = self.get_document_by_id(doc_id)
                    score = pl_entry.score

                    # If the document is already there, don't add a new entry but adapt the score.
                    for item in results:
                        if item.doc == document:
                            item.score += score
                            break
                    result = RequestResult(doc=document, score=score)
                    results.append(result)

        # Sort by descending order of the scores
        results.sort(key=lambda req_res: req_res.score, reverse=True)
        return results


# memory mapped files
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
