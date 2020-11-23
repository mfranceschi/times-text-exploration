import math
from typing import List, final

from doc_parser import pre_work_word
from doc_register import DocRegister
from voc import VOC, VOC_Hashmap
from pl import PL, PLEntry, PL_MMap, ReadOnlyPL

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
        self.read_only_pl: ReadOnlyPL = None

    def register_document(self, doc: Document) -> None:
        self.register += doc

    def compute_scores(self, convert_to_int: bool = True):
        """
        When all documents are parsed, we re-compute scores for all PL entries.
        """
        D = len(self.register)  # Number total of documents

        for voc_entry in self.voc.iterate():
            pl_id = voc_entry.pl_id
            pl_size = voc_entry.pl_size

            current_pl = self.pl.get_pl(pl_id=pl_id, size=pl_size)
            for pl_entry in current_pl:
                tf = 1 + math.log(pl_entry.score)
                idf = math.log(D / (1 + pl_size))
                final_score = 100 * tf * idf
                if convert_to_int:
                    final_score = int(final_score)
                pl_entry.score = final_score

    def generate_mmap_pl(self, pl_file: str):
        total_of_pl_entries = sum(voc_entry.pl_size for voc_entry in self.voc.iterate())
        mmap_file_size = total_of_pl_entries * PL_MMap.PL_ENTRY_LENGTH
        new_pl = PL_MMap(filename=pl_file, filesize=mmap_file_size, mode="write")
        new_voc = VOC_Hashmap()

        for term, voc_entry in self.voc.iterate2():
            pl_to_copy = self.pl.get_pl(voc_entry.pl_id, voc_entry.pl_size)
            pl_id = new_pl.add(pl_to_copy)
            new_voc.add_entry(term, pl_id, voc_entry.pl_size)

        self.pl = new_pl
        self.voc = new_voc

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

    @classmethod
    def read_from_files(cls, voc_file: str, pl_file: str, registry_file: str):
        newinvf = InvertedFile(None, None)
        newinvf.voc = VOC_Hashmap.from_disk(voc_file)
        newinvf.pl = PL_MMap(filename=pl_file, mode="read")
        newinvf.register = DocRegister.from_disk(registry_file)
        return newinvf

    def write_to_files(self, voc_file: str, pl_file: str, registry_file: str):
        self.generate_mmap_pl(pl_file)
        self.voc.to_disk(voc_file)
        self.register.to_disk(registry_file)


"""
MEMORY MAPPED FILES
TODO remove car obsolète

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
