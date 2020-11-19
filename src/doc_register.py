from typing import List, Iterable

from document import Document
import utilities


class DocRegister:
    def __init__(self) -> None:
        self.registry: List[Document] = []

    def add_doc(self, doc: Document) -> None:
        self.registry.append(doc)

    def __iadd__(self, doc: Document) -> None:
        """
        Implements operator +=. Calls 'self.add_doc(doc)'.
        """
        self.add_doc(doc)
        return self

    def get_by_id(self, id: int) -> Document:
        for doc in self.registry:
            if doc.id == id:
                return doc

    def __getitem__(self, id: int) -> Document:
        """
        Implements operator "[id]". Calls 'self.get_document_by_id(id)'.
        """
        return self.get_by_id(id)

    def iterate(self) -> Iterable[Document]:
        for doc in self.registry:
            yield doc

    def __len__(self) -> int:
        return len(self.registry)

    def to_disk(self, name: str) -> None:
        return utilities.write_pyobj_to_disk(self.registry, name)

    @classmethod
    def from_disk(cls, name: str):
        newregistry = DocRegister()
        newregistry.registry = utilities.read_pyobj_from_disk(name)
        return newregistry
