

from typing import List
from doc_parser import parse_document
from inverted_file import InvertedFile
from pl import PL_PythonLists
from utilities import make_list_of_files
from voc import VOC_Hashmap


def main():
    voc = VOC_Hashmap()
    pl = PL_PythonLists()
    nbr_files = 20
    random_files = True

    inverted_file = InvertedFile(voc=voc, pl=pl)
    list_of_files = make_list_of_files(nbr=nbr_files, random_pick=random_files)
    for file in list_of_files:
        parse_document(file, inverted_file)
    inverted_file.compute_scores(convert_to_int=False)

    scores_list: List[float] = []
    for voc_entry in inverted_file.voc.iterate():
        current_pl = inverted_file.pl.get_pl(voc_entry.pl_id, voc_entry.pl_size)
        for pl_entry in current_pl:
            scores_list.append(pl_entry.score)

    print(f"Number of scores: {len(scores_list)}.")
    scores_set = set(scores_list)

    print(f"Number of distinct scores: {len(scores_set)}.")
    scores_list = list(scores_set)
    scores_list.sort()

    print(f"Max score={scores_list[-1]}, min score={scores_list[0]}")
    scores_deltas: List[float] = [0] * (len(scores_list) - 1)
    for i in range(len(scores_list) - 1):
        scores_deltas[i] = scores_list[i+1] - scores_list[i]
    scores_deltas_set = set(scores_deltas)
    scores_deltas_list = list(scores_deltas_set)
    scores_deltas_list.sort()

    print(f"Five minimal score deltas: {scores_deltas_list[:5]}")
    print(f"Five maximal score deltas: {scores_deltas_list[-5:]}")


if __name__ == "__main__":
    main()
