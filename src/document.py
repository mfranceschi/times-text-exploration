
class Document:
    def __init__(self, id: int = 0, title: str = "", no: str = "", text: str = ""):
        self.id = id
        self.title = title
        self.no = no
        self.text = text

    def __str__(self) -> str:
        return f"Document[id={self.id},title={self.title}]"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__):
            return self.id == o.id
        else:
            return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)
