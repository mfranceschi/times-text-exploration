from math import log
from typing import List

from doc_parser import pre_work_word
from doc_register import DocRegister
from voc import VOC
from pl import PL, PLEntry

from document import Document


# https://www.geeksforgeeks.org/python-positional-index/
# https://pypi.org/project/diskhash/


class RequestResult:
    def __init__(self, doc: Document, score: int) -> None:
        self.doc = doc
        self.score = score

    def __str__(self) -> str:
        return f"RequestResult[doc={self.doc}, score={self.score}]"


class InvertedFile:
    def __init__(self, voc: VOC, pl: PL) -> None:
        self.register = DocRegister()
        self.voc: VOC = voc
        self.pl: PL = pl

    def register_document(self, doc: Document) -> None:
        self.register += doc

    def compute_scores(self):
        """
        When all documents are parsed, we re-compute scores for all PL entries.
        """
        D = len(self.register)  # Number total of documents

        for voc_entry in self.voc.iterate():
            pl_id = voc_entry.pl_id
            pl_size = voc_entry.pl_size

            current_pl = self.pl.get_pl(pl_id=pl_id, size=pl_size)
            for pl_entry in current_pl:
                tf = 1 + log(pl_entry.score)
                idf = log(D / (1 + pl_size))
                final_score = int(100 * tf * idf)
                pl_entry.score = final_score

        self.pl = PL.convert_to_readonly(self.pl)

    def notify_word_appeared(self, word: str, docID: int, occurences: int) -> None:
        """
        When parsing a document, this function takes note that the given word appeared in the given file.
        This must not be called several times with the same pair(word, document).
        """
        score = occurences
        if word in self.voc:
            pl_id = self.voc[word].pl_id
            self.pl.update(pl_id, docID, score)
            self.voc.increment_pl_size(word)
        else:
            pl_id = self.pl.create_new_pl(docID, score)
            self.voc.add_entry(word, pl_id)

    def request_words_disjonctive(self, words: List[str]) -> List[RequestResult]:
        """
        Makes an "OR" request of the words.
        The words are preprocessed first.
        """
        request = list(set(pre_work_word(word) for word in words))

        results: List[RequestResult] = []

        for word_to_test in request:
            if word_to_test in self.voc:
                pl_infos = self.voc[word_to_test]
                pl_size = pl_infos.pl_size
                pl_id = pl_infos.pl_id

                pl_for_that_term: List[PLEntry] = self.pl.get_pl(pl_id=pl_id, size=pl_size)

                for pl_entry in pl_for_that_term:
                    doc_id = pl_entry.docID
                    document = self.register[doc_id]
                    score = pl_entry.score

                    # If the document is already there, don't add a new entry but adapt the score.
                    doc_already_here = False
                    for item in results:
                        if item.doc == document:
                            item.score += score
                            doc_already_here = True
                            break
                    if not doc_already_here:
                        result = RequestResult(doc=document, score=score)
                        results.append(result)

        # Sort by descending order of the scores
        results.sort(key=lambda req_res: req_res.score, reverse=True)
        return results

    def request_words_conjonctive(self, words: List[str]) -> List[RequestResult]:
        """
        Makes an "AND" request of the words.
        The words are preprocessed first.
        """
        # idea: same as disjonctive but for each document we ensure that it is in all of the request's word's PLs?
        pass


"""
MEMORY MAPPED FILES

VOC = {paire<"terme",taille PL>, offset PL}
PL = objet continu en disque, accédé en mode "octet par octet".

Idées en vrac:
-> La PL est un tableau continu en mémoire, tableau de paires<docID,score> pour chaque terme.
  - Ainsi, taille et offset nous indiquent où aller et combien d'octets lire
    (par exemple, les 4 premiers octets sont le docID, etc.
  - Problème : mettons que j'ai "dog" dans le doc 1, puis "cat" dans le doc 2.
    J'écris l'entrée pour "cat" au premier emplacement dispo, donc après "dog".
    Maintenant, j'ai encore "dog" dans le doc 3 : il faut que je décalle l'entrée pour "cat" ?
    Et même problème par exemple si un mot comme "London" apparait un doc sur deux, très compliqué.
-> Pareil, mais les paires consécutives ne sont pas associées au même terme,
   et la VOC indiquerait alors une liste d'offsets.
  - On peut paralléliser les accès à la PL pour chaque terme, genre 1 thread par offset.
  - Problème : la mémoire consommée pour stocker la liste d'offsets casse l'intérêt.
    Si la paire de la PL fait 8 octets et mon offset fait 8 octets (typique en 64 bits), c'est con quoi.
-> La PL est un tableau continu en mémoire, tableau de tuples<docID, score, next> pour chaque terme,
   avec "next" l'offset du prochain terme.
  - Logique d'une liste chaînée qui résout les problèmes des ArrayList par exemple.
    Limite on n'a pas besoin de la taille de la PL.
  - Problème : peut-être pas compatible avec les attentes de PEP ?
"""
