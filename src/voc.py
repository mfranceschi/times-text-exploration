from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

from utilities import read_pyobj_from_disk, write_pyobj_to_disk


class VOCEntry:
    """
    This tuple is the value type of the "voc" dict.
    Beign known the word, it gives the Posting List's size and identifier.
    Identifier = how to retrieve it (interpretation changes depending on the PL data structure).
    """

    def __init__(self, pl_identifier: int, size_pl: int) -> None:
        self.pl_id = pl_identifier
        self.pl_size = size_pl

    def __str__(self) -> str:
        return f"VOCEntry[pl_id={self.pl_id}, pl_size={self.pl_size}]"


class VOC:
    """
    VOC Class
    """

    def __init__(self) -> None:
        pass

    def has_term(self, term: str) -> bool:
        """
        Returns true if the given term is in the voc.
        """
        raise NotImplementedError()

    def __contains__(self, term: str) -> bool:
        return self.has_term(term)

    def get_pl_infos(self, term: str) -> VOCEntry:
        """
        Returns infos about the PL of the term.
        """
        raise NotImplementedError()

    def __getitem__(self, term: str) -> VOCEntry:
        return self.get_pl_infos(term)

    def increment_pl_size(self, term: str):
        """
        Just increment by 1 the size of the PL of the given term.
        """
        raise NotImplementedError()

    def add_entry(self, term: str, pl_identifier: int, size: int = 1):
        """
        Adds a new entry to the VOC (identified by the term) with the size of its PL
        """
        raise NotImplementedError()

    def iterate(self) -> Iterable[VOCEntry]:
        """
        Returns an iterable object for running through all the VOCEntries.
        """
        raise NotImplementedError()

    def iterate2(self) -> Iterable[Tuple[str, VOCEntry]]:
        """
        Returns an iterable object for running through all pairs of <term, VOCEntry>.
        """
        raise NotImplementedError()

    def to_disk(self, name: str) -> None:
        """
        Saves the VOC to the disk.
        """
        raise NotImplementedError()

    @classmethod
    def from_disk(cls, name: str) -> None:
        raise NotImplementedError()


class VOC_Hashmap(VOC):

    def __init__(self) -> None:
        super(self.__class__, self).__init__()
        # Associates a word with infos about the PL.
        self.voc: Dict[str, VOCEntry] = defaultdict()

    def has_term(self, term: str) -> bool:
        return not self.voc.get(term) is None

    def get_pl_infos(self, term: str) -> VOCEntry:
        return self.voc.get(term)

    def increment_pl_size(self, term: str) -> None:
        voc_term = self.voc.get(term)
        voc_term.pl_size += 1

    def add_entry(self, term: str, pl_identifier: int, size: int = 1):
        voc_item = VOCEntry(pl_identifier=pl_identifier, size_pl=size)
        self.voc[term] = voc_item

    def iterate(self) -> Iterable[VOCEntry]:
        for entry in self.voc.values():
            yield entry

    def iterate2(self) -> Iterable[Tuple[str, VOCEntry]]:
        for item in self.voc.items():
            yield item

    def to_disk(self, name: str) -> None:
        return write_pyobj_to_disk(self.voc, name)

    @classmethod
    def from_disk(cls, name: str):
        newvoc = VOC_Hashmap()
        newvoc.voc = read_pyobj_from_disk(name)
        return newvoc


# https://pythonhosted.org/BTrees/
# https://btrees.readthedocs.io/en/latest/

# https://pypi.org/project/binarytree/

# https://pypi.org/project/bintrees/

# https://www.tutorialspoint.com/python_data_structure/python_binary_tree.htm#:~:text=To%20insert%20into%20a%20tree,used%20to%20print%20the%20tree.

class VOC_BTree(VOC):

    class Node:
        # Adapted from:
        # https://www.tutorialspoint.com/python_data_structure/python_binary_tree.htm#:~:text=To%20insert%20into%20a%20tree,used%20to%20print%20the%20tree

        class NodeData:
            def __init__(self, term: str, voc_entry: VOCEntry) -> None:
                self.term = term
                self.voc_entry = voc_entry

            def __lt__(self, other):
                if type(other) is VOC_BTree.Node.NodeData:
                    other = self.term
                return self.term < other

            def __gt__(self, other):
                if type(other) is VOC_BTree.Node.NodeData:
                    other = self.term
                return self.term > other

            def __nonzero__(self) -> bool:
                return bool(self.term)

            def __str__(self) -> str:
                return f"NodeData[term={self.term}, entry={self.voc_entry}]"

        def __init__(self, term: str = None, voc_entry: VOCEntry = None):
            self.left: VOC_BTree.Node = None
            self.right: VOC_BTree.Node = None
            if term is None and voc_entry is None:
                self.data = None  # = self.__class__.NodeData(term, voc_entry)
            else:
                self.data = VOC_BTree.Node.NodeData(term, voc_entry)

        def insert(self, term: str, voc_entry: VOCEntry):
            """
            Inserts an entry with the given term and VOC Entry.
            """
            if self.data:
                if term < self.data:
                    if self.left is None:
                        self.left = VOC_BTree.Node(term, voc_entry)
                    else:
                        self.left.insert(term, voc_entry)
                elif term > self.data:
                    if self.right is None:
                        self.right = VOC_BTree.Node(term, voc_entry)
                    else:
                        self.right.insert(term, voc_entry)
            else:
                self.data = VOC_BTree.Node.NodeData(term, voc_entry)

        def findval(self, value: str) -> VOCEntry:
            """
            Returns the VOC Entry if found, else return None.
            """
            if not self.data or not value:
                return None

            if value < self.data:
                if self.left is None:
                    return None
                return self.left.findval(value)
            elif value > self.data:
                if self.right is None:
                    return None
                return self.right.findval(value)
            else:
                return self.data.voc_entry

        def in_order_traversal(self, root=None) -> List[Tuple[str, VOCEntry]]:
            # Adapted from:
            # https://www.tutorialspoint.com/python_data_structure/python_tree_traversal_algorithms.htm
            root: VOC_BTree.Node = root
            res = []
            if root:
                left = self.in_order_traversal(root.left)
                right = self.in_order_traversal(root.right)
                if root.data:
                    data = (root.data.term, root.data.voc_entry)
                    res = [*left, data, *right]
                else:
                    res = [*left, *right]  # Normally it still results in an empty list.
            return res

        def PrintTree(self):
            if self.left:
                self.left.PrintTree()
            print(self.data),
            if self.right:
                self.right.PrintTree()

    class Tree(Node):
        def __init__(self):
            super().__init__()

    def __init__(self) -> None:
        super(self.__class__, self).__init__()
        self.tree = VOC_BTree.Tree()

    def has_term(self, term: str) -> bool:
        return bool(self.tree.findval(term))

    def get_pl_infos(self, term: str) -> VOCEntry:
        return self.tree.findval(term)

    def increment_pl_size(self, term: str):
        voc_entry = self.tree.findval(term)
        if voc_entry:
            voc_entry.pl_size += 1
        else:
            raise KeyError(f"Term '{term}' not found")

    def add_entry(self, term: str, pl_identifier: int, size: int = 1):
        voc_entry = VOCEntry(pl_identifier=pl_identifier, size_pl=size)
        self.tree.insert(term, voc_entry)

    def iterate(self) -> Iterable[VOCEntry]:
        for term, voc_entry in self.tree.in_order_traversal(self.tree):
            yield voc_entry

    def iterate2(self) -> Iterable[Tuple[str, VOCEntry]]:
        for x in self.tree.in_order_traversal(self.tree):
            yield x

    def to_disk(self, name: str):
        return write_pyobj_to_disk(self.tree, name)

    @classmethod
    def from_disk(cls, name: str):
        newvoc = VOC_BTree()
        newvoc.tree = read_pyobj_from_disk(name)
        return newvoc


if __name__ == "__main__":
    vocb = VOC_BTree()
    vocb.add_entry("antony", 18, 0)
    vocb.add_entry("julie", 48, 10)
    vocb.add_entry("bob1", 12, 1)
    vocb.add_entry("bob2", 12, 1)
    vocb.add_entry("bob3", 12, 1)
    vocb.add_entry("bob4", 12, 1)
    vocb.add_entry("bob5", 12, 1)
    vocb.increment_pl_size("antony")

    for term in ["antony", "julie", "toto"]:
        print(f"Term {term} is in voc btree: {vocb.has_term(term)}")

    print("iterate2")
    print([item for item in vocb.iterate2()])

    print()
    print("PrintTree")
    vocb.tree.PrintTree()

    from pathlib import Path
    temp_file_path = Path("voctest.bin")
    vocb.to_disk(temp_file_path)
    vocb2 = VOC_BTree.from_disk(temp_file_path)
    print("PrintTree 2")
    vocb2.tree.PrintTree()
    temp_file_path.unlink(True)
