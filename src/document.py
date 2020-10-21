
from typing import *

from xml.dom import minidom

class Document:
    def __init__(self, id: int=0, title: str="", no: str="", text: str=""):
        self.id = id
        self.title = title
        self.no = no
        self.text = text
    
    def __str__(self) -> str:
        return f"Document[id={self.id},title={self.title}]"
